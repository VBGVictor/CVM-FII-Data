import pandas as pd

def carregar_dados(caminho, filtros=None):
    try:
        df = pd.read_csv(caminho, sep="\t", encoding="latin1", engine="python", error_bad_lines='skip')

        # Aplicar filtros (ex: ?fii=KNRI11&ano=2024)
        if filtros:
            for coluna, valor in filtros.items():
                if coluna in df.columns:
                    df = df[df[coluna].astype(str).str.contains(str(valor), case=False)]

        return df.to_dict(orient="records")

    except Exception as e:
        return {"erro": f"Erro ao carregar dados: {caminho}. Detalhes: {str(e)}"}
