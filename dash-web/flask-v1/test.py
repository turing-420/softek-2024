import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os
from prophet import Prophet

# Directly use the absolute path you've confirmed
file_path = '/workspaces/softek-2024/dash-web/flask-v1/db_softtek/cubo_anl/tbl_full_analitica.xlsx'

# Supercheck function
def supercheck():
    print("Starting supercheck function.")
    
    # Check if file exists
    print(f"Checking if file exists at path: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")
    print("File exists.")
    
    # Load the data
    try:
        print("Loading the data from the Excel file.")
        tbl_anl = pd.read_excel(file_path, engine='openpyxl')
        print("File loaded successfully.")
    except Exception as e:
        raise RuntimeError(f"Error loading the Excel file: {e}")
    
    # Check for required columns
    print("Checking for required columns.")
    required_columns = ['VALOR CONTRATO', 'HORAS', 'STATUS_CHAMADO', 'TIPO_CHAMADO', 'MODULO_CHAMADO', 'COMPLEXIDADE', 'IS', 'CHAMADO', 'SENIORIDADE', 'VALOR_AT', 'DT_ABERTURA_CHAMADO']
    missing_columns = [col for col in required_columns if col not in tbl_anl.columns]
    if missing_columns:
        raise KeyError(f"The following required columns are missing from the data: {missing_columns}")
    print("All required columns are present.")
    
    # Check data types
    print("Checking data types for 'VALOR CONTRATO' and 'HORAS' columns.")
    if not pd.api.types.is_numeric_dtype(tbl_anl['VALOR CONTRATO']):
        raise TypeError("Column 'VALOR CONTRATO' should be of numeric type.")
    print("'VALOR CONTRATO' column is of numeric type.")
    
    if not pd.api.types.is_numeric_dtype(tbl_anl['HORAS']):
        raise TypeError("Column 'HORAS' should be of numeric type.")
    print("'HORAS' column is of numeric type.")
    
    # Additional checks can be added here (e.g., non-null checks, value ranges, etc.)
    print("Supercheck function completed successfully.")

    return tbl_anl

# Run the supercheck
print("Running the supercheck function.")
tbl_anl = supercheck()
print("Supercheck function executed. Data is ready for use.")