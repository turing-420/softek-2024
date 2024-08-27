import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Load data
cubo1_df = pd.read_excel('/workspaces/softek-2024/dash-web/flask-v1/db_softtek/cubo_anl/cubo1_consolidado.xlsx')
cubo2_df = pd.read_excel('/workspaces/softek-2024/dash-web/flask-v1/db_softtek/cubo_anl/cubo2_consolidado.xlsx')
# Define the layout
app.layout = html.Div([
    html.H1("Dashboard de Demandas"),
    
    # Filters
    html.Div([
        html.Label('AnoMes Ref'),
        dcc.Dropdown(id='anomes-dropdown',
                     options=[{'label': anomes, 'value': anomes} for anomes in cubo1_df['ANOMES_REF'].unique()],
                     value=cubo1_df['ANOMES_REF'].unique()[0]),
    ]),
    
    html.Div([
        html.Label('Senioridade'),
        dcc.Dropdown(id='senioridade-dropdown',
                     options=[{'label': s, 'value': s} for s in cubo1_df['SENIORIDADE'].unique()],
                     value=cubo1_df['SENIORIDADE'].unique()[0]),
    ]),

    html.Div([
        html.Label('Área'),
        dcc.Dropdown(id='area-dropdown',
                     options=[{'label': area, 'value': area} for area in cubo1_df['ATRIBUTO'].unique()],
                     value=cubo1_df['ATRIBUTO'].unique()[0]),
    ]),

    html.Div([
        html.Label('Complexidade'),
        dcc.Dropdown(id='complexidade-dropdown',
                     options=[{'label': comp, 'value': comp} for comp in cubo1_df['ATRIBUTO2'].unique()],
                     value=cubo1_df['ATRIBUTO2'].unique()[0]),
    ]),

    # Graphs
    dcc.Graph(id='aberturas-encerramentos-graph'),
    dcc.Graph(id='encerrados-complexidade-graph'),
    dcc.Graph(id='cargo-custo-medio-graph'),
    dcc.Graph(id='encerramentos-cargo-graph'),
    dcc.Graph(id='vol-cargo-complexidade-graph'),
    dcc.Graph(id='tma-cargo-complexidade-graph'),
    dcc.Graph(id='leadtime-graph'),
])

# Define the callbacks

@app.callback(
    Output('aberturas-encerramentos-graph', 'figure'),
    [Input('anomes-dropdown', 'value'),
     Input('senioridade-dropdown', 'value'),
     Input('area-dropdown', 'value'),
     Input('complexidade-dropdown', 'value')]
)
def update_aberturas_encerramentos(selected_anomes, selected_senioridade, selected_area, selected_complexidade):
    filtered_df = cubo1_df[(cubo1_df['ANOMES_REF'] == selected_anomes) & 
                           (cubo1_df['SENIORIDADE'] == selected_senioridade) & 
                           (cubo1_df['ATRIBUTO'] == selected_area) & 
                           (cubo1_df['ATRIBUTO2'] == selected_complexidade)]
    
    if filtered_df.empty:
        return {}
    
    fig = px.bar(filtered_df, x='ATRIBUTO', y='CHAMADO', color='INDICADOR', barmode='group')
    return fig

@app.callback(
    Output('encerrados-complexidade-graph', 'figure'),
    [Input('anomes-dropdown', 'value')]
)
def update_encerrados_complexidade(selected_anomes):
    filtered_df = cubo1_df[(cubo1_df['ANOMES_REF'] == selected_anomes) & (cubo1_df['INDICADOR'] == 'ENCERRAMENTO')]

    # Check if DataFrame is empty or if 'COMPLEXIDADE' column exists
    if filtered_df.empty or 'COMPLEXIDADE' not in filtered_df.columns:
        return px.line()  # Return an empty figure

    # Create the line chart
    fig = px.line(filtered_df, x='ATRIBUTO', y='CHAMADO', color='COMPLEXIDADE')
    return fig

@app.callback(
    Output('cargo-custo-medio-graph', 'figure'),
    [Input('anomes-dropdown', 'value'),
     Input('senioridade-dropdown', 'value'),
     Input('area-dropdown', 'value'),
     Input('complexidade-dropdown', 'value')]
)
def update_cargo_custo_medio(selected_anomes, selected_senioridade, selected_area, selected_complexidade):
    filtered_df = cubo2_df[(cubo2_df['ANOMES_STATUS'] == selected_anomes) & 
                           (cubo2_df['SENIORIDADE'] == selected_senioridade)]
    
    if filtered_df.empty:
        return {}
    
    fig = px.bar(filtered_df, x='SENIORIDADE', y='HORAS', color='COMPLEXIDADE', barmode='group')
    return fig

@app.callback(
    Output('encerramentos-cargo-graph', 'figure'),
    [Input('anomes-dropdown', 'value'),
     Input('senioridade-dropdown', 'value'),
     Input('area-dropdown', 'value'),
     Input('complexidade-dropdown', 'value')]
)
def update_encerramentos_cargo(selected_anomes, selected_senioridade, selected_area, selected_complexidade):
    filtered_df = cubo1_df[(cubo1_df['ANOMES_REF'] == selected_anomes) & 
                           (cubo1_df['SENIORIDADE'] == selected_senioridade) & 
                           (cubo1_df['ATRIBUTO'] == selected_area) & 
                           (cubo1_df['ATRIBUTO2'] == selected_complexidade) & 
                           (cubo1_df['INDICADOR'] == 'ENCERRAMENTO')]
    
    if filtered_df.empty:
        return {}
    
    fig = px.bar(filtered_df, x='ATRIBUTO', y='CHAMADO', color='SENIORIDADE', barmode='group')
    return fig

@app.callback(
    Output('vol-cargo-complexidade-graph', 'figure'),
    [Input('anomes-dropdown', 'value'),
     Input('senioridade-dropdown', 'value'),
     Input('area-dropdown', 'value'),
     Input('complexidade-dropdown', 'value')]
)
def update_vol_cargo_complexidade(selected_anomes, selected_senioridade, selected_area, selected_complexidade):
    filtered_df = cubo1_df[(cubo1_df['ANOMES_REF'] == selected_anomes) & 
                           (cubo1_df['SENIORIDADE'] == selected_senioridade) & 
                           (cubo1_df['ATRIBUTO'] == selected_area) & 
                           (cubo1_df['ATRIBUTO2'] == selected_complexidade) & 
                           (cubo1_df['INDICADOR'] == 'VOLUMETRIA CARGO')]
    
    if filtered_df.empty:
        return {}
    
    fig = px.bar(filtered_df, x='SENIORIDADE', y='CHAMADO', color='ATRIBUTO', barmode='group')
    return fig

@app.callback(
    Output('tma-cargo-complexidade-graph', 'figure'),
    [Input('anomes-dropdown', 'value'),
     Input('senioridade-dropdown', 'value'),
     Input('area-dropdown', 'value'),
     Input('complexidade-dropdown', 'value')]
)
def update_tma_cargo_complexidade(selected_anomes, selected_senioridade, selected_area, selected_complexidade):
    filtered_df = cubo2_df[(cubo2_df['ANOMES_STATUS'] == selected_anomes) & 
                           (cubo2_df['SENIORIDADE'] == selected_senioridade)]
    
    if filtered_df.empty:
        return {}
    
    fig = px.bar(filtered_df, x='SENIORIDADE', y='HORAS', color='COMPLEXIDADE', barmode='group')
    return fig

@app.callback(
    Output('leadtime-graph', 'figure'),
    [Input('anomes-dropdown', 'value')]
)
def update_leadtime(selected_anomes):
    filtered_df = cubo1_df[(cubo1_df['ANOMES_REF'] == selected_anomes) & (cubo1_df['INDICADOR'] == 'LEADTIME')]

    # Check if DataFrame is empty or if 'LEADTIME_CALCULADO' column exists
    if filtered_df.empty or 'LEADTIME_CALCULADO' not in filtered_df.columns:
        return px.bar()  # Return an empty figure

    # Create the bar chart
    fig = px.bar(filtered_df, x='ATRIBUTO', y='CHAMADO', color='LEADTIME_CALCULADO', barmode='group')
    return fig


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
