import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os

def baixar_ipca_mensal():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv"
    df = pd.read_csv(url, sep=';', encoding='utf-8')
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df = df.sort_values('data')
    df['valor'] = df['valor'].str.replace(',', '.').astype(float)
    df = df.rename(columns={'valor': 'IPCA_mensal'})
    return df

def calcular_ipca_12m(df):
    df['IPCA_12m'] = df['IPCA_mensal'].rolling(window=12).sum()
    return df

def calcular_ipca_anual(df):
    df['ano'] = df['data'].dt.year
    ipca_anual = df.groupby('ano')['IPCA_mensal'].sum().reset_index()
    ipca_anual = ipca_anual.rename(columns={'IPCA_mensal': 'IPCA_anual'})
    return df.merge(ipca_anual, on='ano', how='left')

def baixar_cdi_diario():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=csv"
    df = pd.read_csv(url, sep=';', encoding='utf-8')
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df = df.sort_values('data')
    df['valor'] = df['valor'].str.replace(',', '.').astype(float)
    return df.rename(columns={'valor': 'CDI_diario'})

def calcular_cdi_mensal(df):
    df['ano_mes'] = df['data'].dt.to_period('M')
    cdi_mensal = df.groupby('ano_mes')['CDI_diario'].sum().reset_index()
    cdi_mensal['data'] = cdi_mensal['ano_mes'].dt.to_timestamp()
    cdi_mensal = cdi_mensal[['data', 'CDI_diario']].rename(columns={'CDI_diario': 'CDI_mensal'})
    return cdi_mensal

def calcular_cdi_12m(df):
    df['CDI_12m'] = df['CDI_mensal'].rolling(window=12).sum()
    return df

def escolher_pasta_destino():
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.askdirectory(title="Escolha a pasta para salvar o arquivo")
    return caminho

def salvar_csv_sem_duplicatas(df_novo, caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        print("📁 CSV já existe. Verificando dados...")
        df_existente = pd.read_csv(caminho_arquivo, sep=';', parse_dates=['data'])
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        df_final = df_final.drop_duplicates(subset='data').sort_values('data')
    else:
        print("🆕 CSV será criado.")
        df_final = df_novo.copy()

    # Converte colunas numéricas para float (caso estejam como string com vírgula)
    colunas_numericas = df_final.select_dtypes(include=['number', 'object']).columns
    for col in colunas_numericas:
        try:
            # Troca vírgula por ponto e converte para float
            df_final[col] = df_final[col].astype(str).str.replace(',', '.').astype(float)
        except:
            # Se der erro, mantém como está (ex: colunas de data)
            pass

    # Arredonda colunas numéricas para 2 casas decimais
    num_cols = df_final.select_dtypes(include='float').columns
    df_final[num_cols] = df_final[num_cols].round(2)

    # Converte ponto para vírgula só nas colunas numéricas float
    for col in num_cols:
        df_final[col] = df_final[col].apply(lambda x: f"{x:.2f}".replace('.', ','))

    # Salvar CSV com separador ';' e sem index
    try:
        df_final.to_csv(caminho_arquivo, sep=';', index=False, encoding='utf-8-sig')
        print(f"✅ CSV salvo/atualizado em: {caminho_arquivo}")
    except PermissionError:
        print(f"❌ Erro: Arquivo {caminho_arquivo} está aberto em outro programa. Feche-o e tente novamente.")

def executar_coleta_indicadores(pasta_destino: Path):
    """
    Orquestra o download, processamento e salvamento dos dados de IPCA e CDI.
    """
    print("🔄 Baixando dados de indicadores (IPCA x CDI)...")
    ipca_df = baixar_ipca_mensal()
    ipca_df = calcular_ipca_12m(ipca_df)
    ipca_df = calcular_ipca_anual(ipca_df)

    cdi_diario = baixar_cdi_diario()
    cdi_mensal = calcular_cdi_mensal(cdi_diario)
    cdi_mensal = calcular_cdi_12m(cdi_mensal)

    print("📊 Unificando dados...")
    final_df = pd.merge(ipca_df, cdi_mensal, on='data', how='inner')
    final_df = final_df[['data', 'IPCA_mensal', 'IPCA_12m', 'IPCA_anual', 'CDI_mensal', 'CDI_12m']]
    final_df = final_df.dropna()

    caminho_arquivo = pasta_destino / "dados_ipca_cdi.csv"
    salvar_csv_sem_duplicatas(final_df, caminho_arquivo)

if __name__ == "__main__":
    print("Executando IPCAxCDI.py de forma autônoma...")
    pasta = escolher_pasta_destino()
    if pasta:
        executar_coleta_indicadores(Path(pasta))
    else:
        print("❌ Nenhuma pasta selecionada. O programa será encerrado.")
