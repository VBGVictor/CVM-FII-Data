from pathlib import Path
import sys
from CVM_ETL_Inicial import executar_download_cvm
from CVM_Dados_Financeiros import executar_consolidacao_financeira
from CVM_Dados_Qualitativos import executar_consolidacao_qualitativa
from CVM_Dados_Portifolio import executar_consolidacao_portfolio
from app_Scraping import executar_web_scraping

def selecionar_pasta_dados(caminho=None):
    if caminho:
        return Path(caminho)
    else:
        return Path("output/dados_projeto")


def main():
    print("🚀 Iniciando o processo de ETL/ELT para dados de FIIs.")
    print("="*60)

    pasta_arg = sys.argv[1] if len(sys.argv) > 1 else None
    pasta_dados_cvm = selecionar_pasta_dados(pasta_arg)
    print(f"📁 Pasta de dados selecionada: {pasta_dados_cvm}\n")

    executar_download_cvm(pasta_dados_cvm)
    executar_consolidacao_financeira(pasta_dados_cvm)
    executar_consolidacao_qualitativa(pasta_dados_cvm)
    executar_consolidacao_portfolio(pasta_dados_cvm)
    executar_web_scraping(pasta_dados_cvm)

    print("="*60)
    print("✅ Processo finalizado com sucesso!")


if __name__ == "__main__":
    main()
