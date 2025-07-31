import os
import pandas as pd
from pathlib import Path

# Função para processar um único arquivo
def processar_arquivo(caminho):
    try:
        df = pd.read_csv(caminho, sep=';', encoding='utf-8')

        df_resultado = pd.DataFrame()

        df_resultado["Receita Distribuída"] = (
            df.get("Rendimentos_Declarados", 0).fillna(0) +
            df.get("Rendimentos_Pagos_Antecipadamente", 0).fillna(0) +
            df.get("Rendimento_Liquido_Pagar", 0).fillna(0)
        )

        df_resultado["Receita Gerada"] = (
            df.get("Resultado_Trimestral_Liquido_Contabil", 0).fillna(0) +
            df.get("Resultado_Trimestral_Liquido_Financeiro", 0).fillna(0) +
            df.get("Resultado_Liquido_Total_Contabil", 0).fillna(0) +
            df.get("Resultado_Liquido_Total_Financeiro", 0).fillna(0) +
            df.get("Lucro_Contabil", 0).fillna(0)
        ) / 5

        colunas_custos = [col for col in df.columns if 'Custo' in col or 'Despesa' in col or 'Taxa' in col]
        df_resultado["Custos Totais"] = df[colunas_custos].fillna(0).sum(axis=1)

        df_resultado["Receita Aluguel (Contábil)"] = df.get("Receita_Aluguel_Investimento_Contabil", 0).fillna(0)
        df_resultado["Receita Aluguel (Financeiro)"] = df.get("Receita_Aluguel_Investimento_Financeiro", 0).fillna(0)

        # Indício de Vacância
        contab = df.get("Receita_Aluguel_Investimento_Contabil", 0).fillna(0)
        df_resultado["Indício de Vacância"] = (contab - contab.shift(1)).apply(lambda x: "Sim" if x < 0 else "Não")

        # Indício de Inadimplência
        finan = df.get("Receita_Aluguel_Investimento_Financeiro", 0).fillna(0)
        df_resultado["Indício de Inadimplência"] = (contab - finan).apply(lambda x: "Sim" if x > 0 else "Não")

        df_resultado["CNPJ Fundo"] = df["CNPJ_Fundo_Classe"]
        df_resultado["Data de Referência"] = pd.to_datetime(df["Data_Referencia"], errors='coerce')

        # Reordena e limpa
        colunas_ordem = [
            "CNPJ Fundo", "Data de Referência", "Receita Distribuída",
            "Receita Gerada", "Custos Totais",
            "Receita Aluguel (Contábil)", "Receita Aluguel (Financeiro)",
            "Indício de Vacância", "Indício de Inadimplência"
        ]
        df_resultado = df_resultado[colunas_ordem]

        return df_resultado

    except Exception as e:
        print(f"❌ Erro ao processar {caminho}: {e}")
        return None

# Função principal
def executar_consolidacao_financeira(pasta_raiz: Path):
    """
    Consolida os arquivos CSV de resultados financeiros dos FIIs.
    """
    print("--- Módulo 2: Consolidação de Dados Financeiros ---")
    
    dfs = []

    for root, dirs, files in os.walk(pasta_raiz):
        for file in files:
            if file.startswith("inf_trimestral_fii_resultado_contabil_financeiro_") and file.endswith(".csv"):
                caminho_arquivo = os.path.join(root, file)
                df_resultado = processar_arquivo(caminho_arquivo)
                if df_resultado is not None:
                    dfs.append(df_resultado)

    if not dfs:
        print("⚠️ Nenhum arquivo válido encontrado.")
        return

    df_consolidado = pd.concat(dfs, ignore_index=True)
    df_consolidado = df_consolidado.sort_values(by=["CNPJ Fundo", "Data de Referência"])

    caminho_saida = pasta_raiz / "consolidado_financeiro_fiis.csv"
    df_consolidado.to_csv(caminho_saida, sep=';', index=False)

    print(f"✅ Arquivo consolidado gerado: {caminho_saida}")
    print("--- Módulo 2 Concluído! ---\n")
