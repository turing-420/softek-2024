import pandas as pd
import os

caminho = os.path.join('..', '..', 'db_softtek') 
path_arq = os.path.abspath(caminho)
db_orig = '/FIAP_DataBase_v1.xlsx'

# Carrega tabela de demandas:
tbl_demandas = pd.read_excel(path_arq+db_orig, 'DEMANDAS').drop_duplicates()

# Carrega tabela de Contratos:
tbl_contr = pd.read_excel(path_arq+db_orig, 'CONTRATOS').drop_duplicates()

# Carrega tabela de Custos:
tbl_custos = pd.read_excel(path_arq+db_orig, 'CUSTOS').drop_duplicates()
tbl_custos = tbl_custos.groupby(['EXERCICIO','PERIODO','CODIGO_AT']).agg({'VALOR_AT':'mean'}).reset_index()

# Carrega tabela de Equipe:
tbl_equipe = pd.read_excel(path_arq+db_orig, 'EQUIPE').drop_duplicates()

#Demandas x Equipe:

tbl_1 = pd.merge(tbl_demandas, tbl_equipe, how ='left', on = 'IS').fillna(0).drop_duplicates()

# view1 x Custos:
tbl_2  = pd.merge(tbl_1, tbl_custos, how ='left', on = ['EXERCICIO','PERIODO','CODIGO_AT']).drop_duplicates()
#Cruzamento por tbl_2 x contratos:

tbl_3  = pd.merge(tbl_2, tbl_contr, how ='left', left_on = ['PROJETO'],
                  right_on=['PROJETO'])


# Tirando duplicatas por contains de tipo chamado x tipo_demanda:

tbl_3['esta_contido'] = ''
for index, row in tbl_3.iterrows():
    if row['TIPO_CHAMADO'] in row['TIPO_DEMANDA']:
        tbl_3.at[index, 'esta_contido'] = 'Sim'

tbl_3 = tbl_3[tbl_3['esta_contido'] =='Sim'].reset_index().drop(columns=['index','esta_contido']).fillna(0)

tbl_3.describe()
tbl_3.head()
output_folder = os.path.join(path_arq, 'cubo_anl')
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, 'tbl_full_analitica.xlsx')

#Saida primeira Tabela, analitica Full:

tbl_3.to_excel(output_file, index=False)

import pandas as pd
import os
caminho = os.path.join('..', '..', 'db_softtek')
path_arq = os.path.abspath(caminho)

db_analitico = os.path.join(path_arq, 'cubo_anl', 'tbl_full_analitica.xlsx')

# Load
tbl_anl = pd.read_excel(db_analitico, dtype='string').drop_duplicates()

#funções genéricas:


#Função anomes:
def calcul_anomes(df,campo_data):
    if campo_data == 'DT_ABERTURA_CHAMADO':
        nova_coluna = 'ANOMES_ABERTURA'
        df[nova_coluna] = df['DT_ABERTURA_CHAMADO'].astype(str).str[0:4] + df['DT_ABERTURA_CHAMADO'].astype(str).str[5:7]
    else:
        nova_coluna = 'ANOMES_STATUS'
        df[nova_coluna] = df['DT_STATUS_CHAMADO'].astype(str).str[0:4] + df['DT_STATUS_CHAMADO'].astype(str).str[5:7]

    return df

#Função calculo Leadtime de atendimento:
def coluna_leadtime(dias):
    if dias == '0 days':
        return 'D0'
    if dias == '1 days':
        return 'D1'
    elif dias == '2 days':
        return 'D2'
    elif dias == '3 days':
        return 'D3'
    elif dias == '4 days':
        return 'D4'
    else:
        return 'D5+'
#Campo de data abertura do chamado:
tbl_anl['DT_ABERTURA_CHAMADO'] = tbl_anl['DT_ABERTURA_CHAMADO'].astype('datetime64[ns]').dt.strftime("%Y-%m-%d")

#Campo de data status do Chamado:

tbl_anl['DT_STATUS_CHAMADO'] = tbl_anl['EXERCICIO']+"-"+tbl_anl['PERIODO'].str.zfill(2)+"-"+tbl_anl['DIA'].str.zfill(2)
tbl_anl['DT_STATUS_CHAMADO'] = tbl_anl['DT_STATUS_CHAMADO'].astype('datetime64[ns]').dt.strftime("%Y-%m-%d")


# Calcula anomes 
tbl_anl = calcul_anomes(tbl_anl,'DT_ABERTURA_CHAMADO')
tbl_anl = calcul_anomes(tbl_anl,'DT_STATUS_CHAMADO')
tbl_anl = tbl_anl.sort_values(['CHAMADO','DT_ABERTURA_CHAMADO','DT_STATUS_CHAMADO'])

# Criando campos de LeadTime:
tbl_anl['LEADTIME_CHAMADO'] = tbl_anl['DT_STATUS_CHAMADO'].astype('datetime64[ns]') - tbl_anl['DT_ABERTURA_CHAMADO'].astype('datetime64[ns]')
tbl_anl['LEADTIME_CALCULADO'] = tbl_anl['LEADTIME_CHAMADO'].astype(str).apply(coluna_leadtime)

# Indicador de volume de demandas distintas:
tbl_anl_abert = tbl_anl.drop_duplicates(subset=['CHAMADO','DIA','CONSULTOR'], keep='first')
tbl_anl_abert = tbl_anl[['ANOMES_ABERTURA','SENIORIDADE','MODULO_CustosNSULTOR','CHAMADO']].groupby(['ANOMES_ABERTURA','SENIORIDADE','MODULO_CustosNSULTOR']).agg({'CHAMADO':'count'}).reset_index()
tbl_anl_abert['INDICADOR'] = 'ABERTURAS'

tbl_anl_abert.rename(columns={'MODULO_CustosNSULTOR':'ATRIBUTO','ANOMES_ABERTURA':'ANOMES_REF',
                              'SENIORIDADE':'ATRIBUTO2'}, inplace=True)


tbl_anl_abert.head(5)
# Criando base de quantidade de chamados pendentes: 

tbl_anl = tbl_anl.drop_duplicates(subset=['CHAMADO','DIA','CONSULTOR'], keep='last')

tbl_anl_pendentes = tbl_anl[tbl_anl['STATUS_CHAMADO'] !='Closed']
tbl_anl_pendentes = tbl_anl_pendentes[['ANOMES_ABERTURA','SENIORIDADE','COMPLEXIDADE','CHAMADO']].groupby(['ANOMES_ABERTURA','SENIORIDADE','COMPLEXIDADE']).agg({'CHAMADO':'count'}).reset_index()
tbl_anl_pendentes['INDICADOR'] = 'PENDENTE'
tbl_anl_pendentes.rename(columns={'COMPLEXIDADE':'ATRIBUTO','ANOMES_ABERTURA':'ANOMES_REF',
                              'SENIORIDADE':'ATRIBUTO2'}, inplace=True)
tbl_anl_pendentes.head(5)
# Criando base de quantidade de chamados encerrados: 

tbl_anl_encerr = tbl_anl[tbl_anl['STATUS_CHAMADO'] =='Closed']
tbl_anl_encerr = tbl_anl_encerr[['ANOMES_STATUS','SENIORIDADE','MODULO_CustosNSULTOR','CHAMADO']].groupby(['ANOMES_STATUS','SENIORIDADE','MODULO_CustosNSULTOR']).agg({'CHAMADO':'count'}).reset_index()
tbl_anl_encerr['INDICADOR'] = 'ENCERRAMENTO'
tbl_anl_encerr.rename(columns={'MODULO_CustosNSULTOR':'ATRIBUTO','ANOMES_STATUS':'ANOMES_REF',
                              'SENIORIDADE':'ATRIBUTO2'}, inplace=True)
tbl_anl_encerr.head(5)
# Criando base de encerrados e o respectivo Leadtime: 

tbl_anl_long = tbl_anl[tbl_anl['STATUS_CHAMADO'] =='Closed']
tbl_anl_long = tbl_anl_long[['ANOMES_STATUS','LEADTIME_CALCULADO','MODULO_CustosNSULTOR','CHAMADO']].groupby(['ANOMES_STATUS','LEADTIME_CALCULADO','MODULO_CustosNSULTOR']).agg({'CHAMADO':'count'}).reset_index()
tbl_anl_long['INDICADOR'] = 'LEADTIME'
tbl_anl_long.rename(columns={'MODULO_CustosNSULTOR':'ATRIBUTO','ANOMES_STATUS':'ANOMES_REF',
                              'LEADTIME_CALCULADO':'ATRIBUTO2'}, inplace=True)
tbl_anl_long.head(50)
# Criando base de quantidade de complexidade por senioridades: 

tbl_anl_complex = tbl_anl[tbl_anl['STATUS_CHAMADO'] =='Closed']
tbl_anl_complex = tbl_anl_complex[['ANOMES_STATUS','SENIORIDADE','COMPLEXIDADE','CHAMADO']].groupby(['ANOMES_STATUS','SENIORIDADE','COMPLEXIDADE']).agg({'CHAMADO':'count'}).reset_index()
tbl_anl_complex['INDICADOR'] = 'COMPLEXIDADE_VOL'
tbl_anl_complex.rename(columns={'COMPLEXIDADE':'ATRIBUTO','ANOMES_STATUS':'ANOMES_REF',
                              'SENIORIDADE':'ATRIBUTO2'}, inplace=True)
tbl_anl_complex.head(5)
# Criando base de quantidade de encerrados por senioridade: 

tbl_anl_cargo_VOL = tbl_anl[['ANOMES_STATUS','SENIORIDADE','CHAMADO','MODULO_CustosNSULTOR']].groupby(['ANOMES_STATUS','SENIORIDADE','MODULO_CustosNSULTOR']).agg({'CHAMADO':'count'}).reset_index()
tbl_anl_cargo_VOL.rename(columns={'MODULO_CustosNSULTOR':'ATRIBUTO','ANOMES_STATUS':'ANOMES_REF',
                              'LEADTIME_CALCULADO':'ATRIBUTO2'}, inplace=True)
tbl_anl_cargo_VOL['INDICADOR'] = 'VOLUMETRIA CARGO'


tbl_anl_cargo_tma = tbl_anl[['ANOMES_STATUS','SENIORIDADE','COMPLEXIDADE','HORAS','VALOR_AT','CONSULTOR']].drop_duplicates()
tbl_anl_cargo_tma['HORAS'] = round(tbl_anl_cargo_tma['HORAS'].astype('float'),2)
tbl_anl_cargo_tma['VALOR_AT'] = round(tbl_anl_cargo_tma['VALOR_AT'].astype('float'),2)

tbl_anl_cargo_tma = tbl_anl_cargo_tma.groupby(['ANOMES_STATUS','SENIORIDADE','COMPLEXIDADE']).agg({'HORAS':'mean', 'VALOR_AT':'mean'}).reset_index()
tbl_anl_cargo_tma.head(5)
#concatenando todos os dados em um cubo único chamado cubo_1:

cubo_1 = pd.concat([tbl_anl_abert,tbl_anl_encerr,tbl_anl_long,tbl_anl_pendentes,tbl_anl_complex,tbl_anl_cargo_VOL], axis=0)
#Indicador de Aberturas x Encerramentos:

abr_x_encerr = pd.merge(
                tbl_anl_abert.groupby(['ANOMES_REF']).agg({'CHAMADO':'sum'}).reset_index().rename(columns={'CHAMADO':'ABERTURAS'}),
                tbl_anl_encerr.groupby(['ANOMES_REF']).agg({'CHAMADO':'sum'}).reset_index().rename(columns={'CHAMADO':'ENCERRADOS'})
, how = 'left', on = 'ANOMES_REF').fillna(0)

abr_x_encerr['% Aberturas x Encerrados'] = round((abr_x_encerr['ENCERRADOS'] / abr_x_encerr['ABERTURAS']) * 100, 2)
abr_x_encerr = abr_x_encerr[abr_x_encerr['ANOMES_REF'] >= '202401']


#Indicador de Volume de ocorrências x Complexidade:

pivot_complex = tbl_anl_complex[tbl_anl_complex['INDICADOR'] == 'COMPLEXIDADE_VOL'].pivot_table(
    index='ANOMES_REF',
    columns='ATRIBUTO',
    values='CHAMADO',
    aggfunc='sum'
).reset_index()
pivot_complex.columns.name = None

pivot_complex
#Indicador de Volume de Senioridade x Custo médio em R$:

pivot_ctm = tbl_anl_cargo_tma.pivot_table(
    index='ANOMES_STATUS',
    columns='SENIORIDADE',
    values='VALOR_AT',
    aggfunc='mean'
).reset_index()
pivot_ctm.columns.name = None

pivot_ctm
#Indicador de Volume de Senioridade x Encerramentos:

pivot_enc_sen = cubo_1[cubo_1['INDICADOR'] == 'VOLUMETRIA CARGO'].pivot_table(
    index='ANOMES_REF',
    columns='SENIORIDADE',
    values='CHAMADO',
    aggfunc='sum'
).reset_index()

pivot_enc_sen.columns.name = None

pivot_enc_sen
#Indicador de LEADTIME de encerrados mes a mes:

pivot_LEAD = cubo_1[cubo_1['INDICADOR'] == 'LEADTIME'].pivot_table(
    index='ANOMES_REF',
    columns='ATRIBUTO2',
    values='CHAMADO',
    aggfunc='sum'
).reset_index()

pivot_LEAD.columns.name = None

pivot_LEAD
# Define the output folder path
output_folder = os.path.join(path_arq, 'cubo_anl')

# Create the folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Export the JSON files
json1 = abr_x_encerr.reset_index().drop(columns='index').to_json(os.path.join(output_folder, 'aberturas_encerrados.json'), orient='records', indent=4)
json2 = pivot_complex.reset_index().drop(columns='index').to_json(os.path.join(output_folder, 'encerrados_complexidade.json'), orient='records', indent=4)
json3 = pivot_ctm.reset_index().drop(columns='index').to_json(os.path.join(output_folder, 'senioridade_custo.json'), orient='records', indent=4)
json4 = pivot_enc_sen.reset_index().drop(columns='index').to_json(os.path.join(output_folder, 'encerramento_senioridade.json'), orient='records', indent=4)
json5 = pivot_LEAD.reset_index().drop(columns='index').to_json(os.path.join(output_folder, 'leadtime_mes_a_mes.json'), orient='records', indent=4)

print("JSON files exported successfully.")
import pandas as pd
import os
import matplotlib.pyplot as plt

caminho = os.path.join('..', '..', 'db_softtek')
path_arq = os.path.abspath(caminho)
# Define the analytic Excel file path
tbl_analitico_path = os.path.join(path_arq, 'cubo_anl', 'tbl_full_analitica.xlsx')

# Load the Excel file
tbl_anl = pd.read_excel(tbl_analitico_path)

#verificando se há valores nulos no data set:

tbl_anl.isnull().sum()
tbl_anl.dtypes
# tipando campos necessários:

tbl_anl['VALOR CONTRATO'] = tbl_anl['VALOR CONTRATO'].astype(float)
tbl_anl.describe()
## Regras de negócio:

# 1 - Melhorar eficiencia em horas do volume de tratativas
# 2 - Melhorar a distribuição de demandas de acordo com o capacity de cada operador
# 3 - Melhorar a relação de custos de acordo com o capacity

tbl_anl.HORAS.plot(kind='box')
plt.title('Boxplot para a variavel horas')
plt.ylabel('tempo em horas')
plt.show()
# Solução para variável horas: Dividir em grupos de forma categorizada


# Função que verificaa o intervalo e retornar a marcação correspondente:

def verifica_intervalo(valor):
    if 0 < valor <= 2:
        return 'MAIOR que 0 e MENOR OU IGUAL a 2' # media
    elif 2 < valor <= 4:
        return 'MAIOR que 2 e MENOR OU IGUAL a 4' # media superior
    elif 4 < valor <= 6:
        return 'MAIOR que 4 e MENOR OU IGUAL a 6' # cauda
    elif valor > 6:
        return 'MAIOR que 6' # Outliers
    else:
        return 'fora dos intervalos' # dados invalidos


tbl_anl['intervalo_horas']= tbl_anl['HORAS'].apply(verifica_intervalo)
# validação da marcação:

tbl_anl[['HORAS','intervalo_horas']]
tbl_anl.VALOR_AT.plot(kind='hist',bins=10)
plt.axvline(tbl_anl.VALOR_AT.quantile(q=0.025), c='r')
plt.axvline(tbl_anl.VALOR_AT.quantile(q=0.975), c='r')    
plt.title('Histograma da variavel de Custos')
## Conclusão do histograma de valores: 

# Frequencia de valores acima de 97,5% é muito pequena (pode ser tratado de outra forma no modelo)
tbl_consultor = tbl_anl[tbl_anl['STATUS_CHAMADO'] == 'Closed']
tbl_consultor = tbl_consultor.groupby(['IS','MODULO_CHAMADO','TIPO_CHAMADO','MODULO_CustosNSULTOR','COMPLEXIDADE','SENIORIDADE']).agg(
    {'HORAS':'min','VALOR_AT':'min','CHAMADO':'count'}).reset_index()
tbl_consultor2 = tbl_consultor.groupby(['TIPO_CHAMADO','MODULO_CHAMADO','COMPLEXIDADE','IS','SENIORIDADE']).agg({'CHAMADO':'mean','HORAS':'min',
                                                                                         'VALOR_AT':'min'}).reset_index().sort_values(
                                                                                             ['TIPO_CHAMADO', 'MODULO_CHAMADO','COMPLEXIDADE',
                                                                                             'CHAMADO','HORAS','VALOR_AT'],
                                                                                               ascending=[True,True, True, False,True,True]
                                                                                               )
tbl_consultor2
# Normalizando as métricas de forma linear ponderada

tbl_consultor2['volume_normalizado'] = tbl_consultor2['CHAMADO'] / tbl_consultor2['CHAMADO'].max()

# Invertendo a normalização para que menor valor de horas por chamado seja melhor
tbl_consultor2['horas_normalizado'] = 1 - (tbl_consultor2['HORAS'] / tbl_consultor2['HORAS'].max())

# Invertendo a normalização para que menor valor de custo por chamado seja melhor
tbl_consultor2['custo_normalizado'] = 1 - (tbl_consultor2['VALOR_AT'] / tbl_consultor2['VALOR_AT'].max())
# Definindo os pesos para cada métrica:

peso_volume = 0.5
peso_horas = 0.3
peso_custo = 0.2
# Calculando o score de eficiência combinando os valores ponderados
tbl_consultor2['score_eficiencia'] = (
    (tbl_consultor2['volume_normalizado'] * peso_volume) + 
    (tbl_consultor2['horas_normalizado'] * peso_horas) + 
    (tbl_consultor2['custo_normalizado'] * peso_custo)
)
tbl_consultor3 = tbl_consultor2[['TIPO_CHAMADO', 'MODULO_CHAMADO','COMPLEXIDADE','IS','score_eficiencia','CHAMADO','SENIORIDADE']]
tbl_consultor3['rank'] = tbl_consultor3.groupby(['TIPO_CHAMADO', 'MODULO_CHAMADO','COMPLEXIDADE'])['score_eficiencia'].rank(ascending=False, method='dense')
tbl_consultor3.sort_values(['TIPO_CHAMADO', 'MODULO_CHAMADO','COMPLEXIDADE','rank'], inplace=True)

tbl_consultor3.head(50)
output_folder_modelo = os.path.join(path_arq, 'modelo')

os.makedirs(output_folder_modelo, exist_ok=True)

output_file_modelo = os.path.join(output_folder_modelo, 'Modelo_score_train.xlsx')

tbl_consultor4 = tbl_consultor3.groupby(['TIPO_CHAMADO', 'MODULO_CHAMADO', 'COMPLEXIDADE', 'IS']) \
    .agg({'rank': 'min', 'score_eficiencia': 'max'}) \
    .reset_index() \
    .sort_values(['TIPO_CHAMADO', 'MODULO_CHAMADO', 'COMPLEXIDADE', 'IS', 'rank']) \
    .drop_duplicates(subset='IS', keep='first')

tbl_consultor4.to_excel(output_file_modelo, index=False)

print(f"Score salvo: {output_file_modelo}")

tbl_consultor4.sort_values(['TIPO_CHAMADO','MODULO_CHAMADO','COMPLEXIDADE','rank'])
import pandas as pd
from itertools import cycle
import shutil
import os
caminho = os.path.join('..', '..', 'db_softtek') 
path_arq = os.path.abspath(caminho) 
tbl_train_path = os.path.join(path_arq, 'modelo', 'Modelo_score_train.xlsx')
tbl_test_path = os.path.join(path_arq, 'cubo_anl', 'tbl_full_analitica.xlsx')

tbl_train = pd.read_excel(tbl_train_path)
analistas_df = tbl_train
# Load the test data (tbl_full_analitica.xlsx)
tbl_test = pd.read_excel(tbl_test_path)

# Filter out necessary columns from the test data (novos chamados)
novos_chamados_df = tbl_test[['CHAMADO', 'DT_ABERTURA_CHAMADO', 'TIPO_CHAMADO', 'MODULO_CHAMADO', 'COMPLEXIDADE']].drop_duplicates(keep='first')

# Agrupar analistas por módulo e ordenar por rank
analistas_por_modulo = analistas_df.sort_values(by=['MODULO_CHAMADO', 'rank']).groupby('MODULO_CHAMADO')

# Criar iteradores rotativos para cada módulo
iteradores = {modulo: cycle(grupo['IS'].tolist()) for modulo, grupo in analistas_por_modulo}

# Função para distribuir chamados
def distribuir_chamados(novos_chamados_df, iteradores):
    alocacao = []
    for _, chamado in novos_chamados_df.iterrows():
        modulo = chamado['MODULO_CHAMADO']
        if modulo in iteradores:
            analista = next(iteradores[modulo])
            alocacao.append(analista)
        else:
            alocacao.append(None)  # Caso não haja analistas para o módulo
    return alocacao

# Distribuir os novos chamados
novos_chamados_df['IS'] = distribuir_chamados(novos_chamados_df[['TIPO_CHAMADO','MODULO_CHAMADO','COMPLEXIDADE']], iteradores)

# Exibir a distribuição
novos_chamados_df.sort_values(['TIPO_CHAMADO','MODULO_CHAMADO']).ffill()
novos_chamados_df['ANOMES_ABERTURA'] = novos_chamados_df['DT_ABERTURA_CHAMADO'].str[0:4] + novos_chamados_df['DT_ABERTURA_CHAMADO'].str[5:7]


# Criando Pivot Table para os gráficos:

pivot_REDIST = novos_chamados_df.pivot_table(
    index='ANOMES_ABERTURA',
    columns='COMPLEXIDADE',
    values='CHAMADO',
    aggfunc='count'
).reset_index().fillna(0)

pivot_REDIST.columns.name = None

pivot_REDIST = pivot_REDIST[pivot_REDIST['ANOMES_ABERTURA'] >= '202401']
pivot_REDIST
# Output
output_folder_modelo = os.path.join(path_arq, 'modelo')
os.makedirs(output_folder_modelo, exist_ok=True)

output_excel_path = os.path.join(output_folder_modelo, 'alocacao_recursos.xlsx')
pivot_REDIST.to_excel(output_excel_path, index=False)
print(f"EXCEL salvo: {output_excel_path}")

output_json_path = os.path.join(output_folder_modelo, 'cubo3_alocacao_recursos.json')
pivot_REDIST.reset_index().drop(columns='index').to_json(output_json_path, orient='records', indent=4)
print(f"JSON salvo: {output_json_path}")
# Definir caminhos
caminho_base = os.path.abspath(os.path.join('..', '..', 'db_softtek'))
caminho_cubo_anl = os.path.join(caminho_base, 'cubo_anl')
caminho_modelo = os.path.join(caminho_base, 'modelo')
caminho_dados_frontend = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'frontend', 'data'))

# Garantir que o diretório de destino exista
if not os.path.exists(caminho_dados_frontend):
    print(f"Criando diretório '{caminho_dados_frontend}'\n")
    os.makedirs(caminho_dados_frontend)
else:
    print(f"'{caminho_dados_frontend}' já existe\n")

# Lista de arquivos JSON para copiar
arquivos_json = [
    'aberturas_encerrados.json',
    'leadtime_mes_a_mes.json',
    'encerrados_complexidade.json',
    'senioridade_custo.json',
    'encerramento_senioridade.json'
]

# Copiar arquivos JSON do diretório cubo_anl para a pasta de dados do frontend
for nome_arquivo in arquivos_json:
    origem = os.path.join(caminho_cubo_anl, nome_arquivo)
    destino = os.path.join(caminho_dados_frontend, nome_arquivo)
    if os.path.exists(origem):
        try:
            shutil.copy(origem, destino)
            print(f"'{nome_arquivo}' salvo: '{destino}'\n")
        except Exception as e:
            print(f"Erro ao copiar '{nome_arquivo}': {e}\n")
    else:
        print(f"Arquivo '{nome_arquivo}' não encontrado em {caminho_cubo_anl}\n")

# Copiar e renomear o arquivo JSON específico
origem_cubo3 = os.path.join(caminho_modelo, 'cubo3_alocacao_recursos.json')
destino_cubo3 = os.path.join(caminho_dados_frontend, 'acompanhamento_da_redistribuicao.json')

if os.path.exists(origem_cubo3):
    try:
        shutil.copy(origem_cubo3, destino_cubo3)
        print(f"'cubo3_alocacao_recursos.json' salvo: '{destino_cubo3}'\n")
    except Exception as e:
        print(f"Erro ao copiar 'cubo3_alocacao_recursos.json': {e}\n")
else:
    print(f"Arquivo 'cubo3_alocacao_recursos.json' não encontrado em {caminho_modelo}\n")

print('Todos os arquivos processados.\n')
# Salva o CSV com a alocação dos novos chamados para email_notif.ipynb
csv_path = os.path.join(output_folder_modelo, 'novos_chamados.csv')
novos_chamados_df.to_csv(csv_path, index=False)
print(f"CSV salvo: {csv_path}")