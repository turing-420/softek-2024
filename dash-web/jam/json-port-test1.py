import pandas as pd
import json

cubo1_df = pd.read_excel('data/cubo1_consolidado.xlsx')
cubo2_df = pd.read_excel('data/cubo2_consolidado.xlsx')

cubo1_filtered = cubo1_df[cubo1_df['ANOMES_REF'].between(202401, 202404)]
cubo2_filtered = cubo2_df[cubo2_df['ANOMES_STATUS'].between(202401, 202404)]

aberturas_encerramento = cubo1_filtered.groupby('ANOMES_REF').agg(
    ABERTURAS=('CHAMADO', 'sum'),
    ENCERRAMENTO=('CHAMADO', 'sum')
).reset_index()

aberturas_encerramento['%_ADERENCIA'] = (aberturas_encerramento['ENCERRAMENTO'] / aberturas_encerramento['ABERTURAS']) * 100
aberturas_encerramento['%_ADERENCIA'] = aberturas_encerramento['%_ADERENCIA'].round(1)

encerrados_complexidade = cubo2_filtered.pivot_table(
    index='ANOMES_STATUS',
    columns='COMPLEXIDADE',
    values='VALOR_AT',
    aggfunc='count',
    fill_value=0
).reset_index()

custo_medio_por_demanda = cubo2_filtered.groupby(['SENIORIDADE', 'ANOMES_STATUS']).agg(
    CUSTO_MEDIO=('VALOR_AT', 'mean')
).reset_index()

encerramentos_cargo = cubo2_filtered.groupby(['SENIORIDADE', 'ANOMES_STATUS']).agg(
    ENCERRAMENTOS=('VALOR_AT', 'count')
).reset_index()

vol_cargo_complexidade = cubo2_filtered.groupby(['SENIORIDADE', 'COMPLEXIDADE']).agg(
    VOLUME=('VALOR_AT', 'count')
).reset_index()

area_options = cubo1_filtered['ATRIBUTO'].unique().tolist()

dashboard_json = {
    "aberturas_encerramento": aberturas_encerramento.to_dict(orient='records'),
    "encerrados_complexidade": encerrados_complexidade.to_dict(orient='records'),
    "custo_medio_por_demanda": custo_medio_por_demanda.to_dict(orient='records'),
    "encerramentos_cargo": encerramentos_cargo.to_dict(orient='records'),
    "vol_cargo_complexidade": vol_cargo_complexidade.to_dict(orient='records'),
    "area_options": area_options
}

with open('dashboard.json', 'w') as f:
    json.dump(dashboard_json, f, indent=4)


with open('dashboard.json', 'w') as f:
    json.dump(dashboard_json, f, indent=4)

print(json.dumps(dashboard_json, indent=4))
