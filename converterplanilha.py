import pandas as pd

# Caminho para a planilha do Excel
caminho_planilha = '/home/pablito/meu_gpt/planilhas/bncc_educacao_infantil.xlsx'

# Carrega a planilha do Excel
excel_file = pd.ExcelFile(caminho_planilha)

# Itera sobre cada aba da planilha
for sheet_name in excel_file.sheet_names:
    # Lê os dados da aba atual
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Constrói o nome do arquivo CSV
    csv_file_name = f"{sheet_name}.csv"
    
    # Salva os dados da aba em um arquivo CSV
    df.to_csv(csv_file_name, index=False)
    
    print(f"Aba '{sheet_name}' salva como '{csv_file_name}'.")
