import os
import pandas as pd
from pathlib import Path

def corrigir_codificacao(df):
    df.columns = [col.encode('latin1').decode('utf-8') for col in df.columns]
    return df

def processar_arquivo(path_arquivo, ano):
    df = pd.read_csv(path_arquivo, sep=';', encoding='latin1')
    df = corrigir_codificacao(df)
    df["Ano de Referência"] = ano
    return df

def consolidar_e_salvar(nome_base, nome_saida, pasta_dados: Path):
    arquivos_encontrados = []
    for root, _, files in os.walk(pasta_dados):
        for file in files:
            if file.startswith(nome_base) and file.endswith(".csv"):
                ano = ''.join(filter(str.isdigit, file))
                arquivos_encontrados.append((os.path.join(root, file), ano))
    
    todos_dfs = []

    for caminho, ano in arquivos_encontrados:
        try:
            df = processar_arquivo(caminho, ano)
            todos_dfs.append(df)
        except Exception as e:
            print(f"Erro ao processar {caminho}: {e}")

    if todos_dfs:
        df_final = pd.concat(todos_dfs, ignore_index=True)
        caminho_saida = pasta_dados / nome_saida
        df_final.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
        print(f"✅ Arquivo consolidado gerado: {caminho_saida}")
    else:
        print(f"Nenhum arquivo encontrado para {nome_base}.")

def executar_consolidacao_portfolio(pasta_dados: Path):
    """
    Consolida os arquivos CSV de dados de portfólio (ativos e imóveis) dos FIIs.
    """
    print("--- Módulo 4: Consolidação de Dados de Portfólio ---")
    consolidar_e_salvar("inf_trimestral_fii_ativo_", "consolidado_fii_ativo.csv", pasta_dados)
    consolidar_e_salvar("inf_trimestral_fii_imovel_desempenho_", "consolidado_fii_imovel_desempenho.csv", pasta_dados)
    print("--- Módulo 4 Concluído! ---\n")
