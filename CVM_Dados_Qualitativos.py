import os
import pandas as pd
from pathlib import Path

def corrigir_codificacao(df):
    df.columns = [col.encode('latin1').decode('utf-8') for col in df.columns]
    return df

def processar_arquivo_geral(path_arquivo, ano):
    df = pd.read_csv(path_arquivo, sep=';', encoding='latin1')
    df = corrigir_codificacao(df)
    df["Ano de Referência"] = ano
    return df

def executar_consolidacao_qualitativa(pasta_dados: Path):
    """
    Consolida os arquivos CSV de dados gerais (qualitativos) dos FIIs.
    """
    print("--- Módulo 3: Consolidação de Dados Qualitativos ---")
    nome_base_arquivo = "inf_trimestral_fii_geral_"
    arquivos_encontrados = []
    
    for root, _, files in os.walk(pasta_dados):
        for file in files:
            if file.startswith(nome_base_arquivo) and file.endswith(".csv"):
                ano = ''.join(filter(str.isdigit, file))
                arquivos_encontrados.append((os.path.join(root, file), ano))

    todos_dfs = []
    for caminho, ano in arquivos_encontrados:
        try:
            df = processar_arquivo_geral(caminho, ano)
            todos_dfs.append(df)
        except Exception as e:
            print(f"Erro ao processar {caminho}: {e}")

    if not todos_dfs:
        print("Nenhum arquivo processado.")
        return
        
    df_final = pd.concat(todos_dfs, ignore_index=True)
    caminho_saida = pasta_dados / "consolidado_fii_geral.csv"
    df_final.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"✅ Arquivo consolidado gerado: {caminho_saida}")
    print("--- Módulo 3 Concluído! ---\n")
