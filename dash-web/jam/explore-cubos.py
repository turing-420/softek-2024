import pandas as pd

file_path_1 = 'data/cubo1_consolidado.xlsx'
file_path_2 = 'data/cubo2_consolidado.xlsx'

df_cubo1 = pd.read_excel(file_path_1)
df_cubo2 = pd.read_excel(file_path_2)

def clean_and_print_df_summary(df, name):
    print(f"--- {name} DataFrame ---")
    df.columns = df.columns.str.strip()
    
    print("Columns:")
    print(df.columns)
    print("\nFirst 5 Rows:")
    print(df.head())
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isna().sum())
    print("\nSummary Statistics:")
    print(df.describe(include='all'))

clean_and_print_df_summary(df_cubo1, 'Cubo1')
clean_and_print_df_summary(df_cubo2, 'Cubo2')
def check_for_trailing_characters(df, name):
    print(f"\n{name} Columns after stripping:")
    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].apply(lambda x: isinstance(x, str) and x != x.strip()).any():
                print(f"Trailing characters found in column: {col}")

check_for_trailing_characters(df_cubo1, 'Cubo1')
check_for_trailing_characters(df_cubo2, 'Cubo2')
