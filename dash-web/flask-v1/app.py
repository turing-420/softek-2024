import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os
from prophet import Prophet

file_path = '/workspaces/softek-2024/dash-web/flask-v1/db_softtek/cubo_anl/tbl_full_analitica.xlsx'

try:
    tbl_anl = pd.read_excel(file_path, engine='openpyxl')
    print("File loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: {e}")

def preprocess_data(tbl_anl):

    tbl_anl['VALOR CONTRATO'] = tbl_anl['VALOR CONTRATO'].astype(float)

    def verifica_intervalo(valor):
        if 0 < valor <= 2:
            return 'MAIOR que 0 e MENOR OU IGUAL a 2'
        elif 2 < valor <= 4:
            return 'MAIOR que 2 e MENOR OU IGUAL a 4'
        elif 4 < valor <= 6:
            return 'MAIOR que 4 e MENOR OU IGUAL a 6'
        elif valor > 6:
            return 'MAIOR que 6'
        else:
            return 'fora dos intervalos'

    tbl_anl['intervalo_horas'] = tbl_anl['HORAS'].apply(verifica_intervalo)


    tbl_consultor = tbl_anl.loc[tbl_anl['STATUS_CHAMADO'] == 'Closed']


    tbl_consultor2 = tbl_consultor.groupby(['TIPO_CHAMADO','MODULO_CHAMADO','COMPLEXIDADE','IS','SENIORIDADE']).agg({
        'CHAMADO': 'count', 
        'HORAS': 'min',     
        'VALOR_AT': 'min'   
    }).reset_index()

    tbl_consultor2['volume_normalizado'] = tbl_consultor2['CHAMADO'] / tbl_consultor2['CHAMADO'].max()
    tbl_consultor2['horas_normalizado'] = 1 - (tbl_consultor2['HORAS'] / tbl_consultor2['HORAS'].max())
    tbl_consultor2['custo_normalizado'] = 1 - (tbl_consultor2['VALOR_AT'] / tbl_consultor2['VALOR_AT'].max())

    peso_volume = 0.5
    peso_horas = 0.3
    peso_custo = 0.2

    tbl_consultor2['score_eficiencia'] = (
        (tbl_consultor2['volume_normalizado'] * peso_volume) + 
        (tbl_consultor2['horas_normalizado'] * peso_horas) + 
        (tbl_consultor2['custo_normalizado'] * peso_custo)
    )

    tbl_consultor3 = tbl_consultor2[['TIPO_CHAMADO', 'MODULO_CHAMADO','COMPLEXIDADE','IS','score_eficiencia','CHAMADO','SENIORIDADE', 'HORAS', 'VALOR_AT']].copy()

    tbl_consultor3['rank'] = tbl_consultor3.groupby(['TIPO_CHAMADO', 'MODULO_CHAMADO','COMPLEXIDADE'])['score_eficiencia'].rank(ascending=False, method='dense')

    return tbl_consultor3

tbl_anl_preprocessed = preprocess_data(tbl_anl)

consultor_options = [{'label': i, 'value': i} for i in tbl_anl_preprocessed['SENIORIDADE'].unique() if pd.notnull(i)]
modulo_options = [{'label': i, 'value': i} for i in tbl_anl_preprocessed['MODULO_CHAMADO'].unique() if pd.notnull(i)]
complexidade_options = [{'label': i, 'value': i} for i in tbl_anl_preprocessed['COMPLEXIDADE'].unique() if pd.notnull(i)]

def add_predictive_modeling(df):

    df['ds'] = pd.to_datetime(df['DT_ABERTURA_CHAMADO'], format='%Y-%m-%d')
    df['y'] = df['CHAMADO'].astype(int)
    
    model = Prophet()
    model.fit(df[['ds', 'y']])

    future = model.make_future_dataframe(periods=30) 

    forecast = model.predict(future)
    
    return forecast

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Demandas"),


    dcc.Dropdown(id='consultor-dropdown', options=consultor_options, placeholder='Selecionar Consultor'),
    dcc.Dropdown(id='modulo-dropdown', options=modulo_options, placeholder='Selecionar Módulo'),
    dcc.Dropdown(id='complexidade-dropdown', options=complexidade_options, placeholder='Selecionar Complexidade'),

    dcc.Graph(id='eficiencia-graph'),
    dcc.Graph(id='horas-graph'),
    dcc.Graph(id='custo-graph'),
    
    dcc.Graph(id='previsao-graph'), 


    html.Div(id='tabela-dinamica')
])

@app.callback(
    [Output('eficiencia-graph', 'figure'),
     Output('horas-graph', 'figure'),
     Output('custo-graph', 'figure'),
     Output('tabela-dinamica', 'children'),
     Output('previsao-graph', 'figure')], 
    [Input('consultor-dropdown', 'value'),
     Input('modulo-dropdown', 'value'),
     Input('complexidade-dropdown', 'value')]
)
def update_graphs(selected_consultor, selected_modulo, selected_complexidade):
    df_filtered = tbl_anl_preprocessed.copy()

    if selected_consultor:
        df_filtered = df_filtered[df_filtered['SENIORIDADE'] == selected_consultor]
    if selected_modulo:
        df_filtered = df_filtered[df_filtered['MODULO_CHAMADO'] == selected_modulo]
    if selected_complexidade:
        df_filtered = df_filtered[df_filtered['COMPLEXIDADE'] == selected_complexidade]


    if df_filtered.empty:
        return {}, {}, {}, html.Table(), {} 

    fig_eficiencia = px.bar(df_filtered, x='IS', y='score_eficiencia', color='COMPLEXIDADE', title='Score de Eficiência por Consultor')
    fig_horas = px.histogram(df_filtered, x='HORAS', nbins=10, title='Distribuição de Horas')
    fig_custo = px.histogram(df_filtered, x='VALOR_AT', nbins=10, title='Distribuição de Custos')

    tabela_dinamica = df_filtered.groupby(['IS', 'MODULO_CHAMADO']).agg({
        'CHAMADO': 'count',
        'HORAS': 'mean',
        'VALOR_AT': 'mean'
    }).reset_index()

    tabela_html = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in tabela_dinamica.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(tabela_dinamica.iloc[i][col]) for col in tabela_dinamica.columns
            ]) for i in range(len(tabela_dinamica))
        ])
    ])

    forecast = add_predictive_modeling(df_filtered)

    fig_previsao = px.line(forecast, x='ds', y='yhat', title='Forecast of Demand')

    return fig_eficiencia, fig_horas, fig_custo, tabela_html, fig_previsao 

if __name__ == '__main__':
    app.run_server(debug=True)