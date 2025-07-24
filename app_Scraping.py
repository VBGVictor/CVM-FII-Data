from pathlib import Path
import sys

# Importações dos seus módulos
from FII_Explorer import executar_scraping_fii_explorer
from FII_Investing import executar_scraping_fii_investing
from IPCAxCDI import executar_coleta_indicadores


def selecionar_pasta_destino(caminho_manual=None) -> Path:
    """
    Retorna o caminho da pasta de destino.
    Se um caminho for passado como argumento, usa ele. Caso contrário,
    define uma pasta padrão (output/dados_scraping).
    """
    if caminho_manual:
        return Path(caminho_manual)
    else:
        caminho_padrao = Path("output/dados_scraping")
        caminho_padrao.mkdir(parents=True, exist_ok=True)
        return caminho_padrao


def executar_web_scraping(pasta_destino: Path):
    """
    Função que orquestra a execução dos scripts de web scraping e coleta de indicadores.
    """
    print("\n--- Módulo 5: Executando Coleta de Dados Externos (Scraping e APIs) ---")
    print(f"📁 Arquivos de dados externos serão salvos em: {pasta_destino}\n")

    # --- Sub-módulo 5.1: Coleta de Indicadores (IPCA x CDI) ---
    try:
        print("--- Executando coleta de indicadores (IPCA x CDI) ---")
        executar_coleta_indicadores(pasta_destino)
        print("--- Coleta de indicadores Concluída! ---\n")
    except Exception as e:
        print(f"❌ Erro ao executar a coleta de indicadores: {e}\n")

    # --- Sub-módulo 5.2: Executar o scraping do Funds Explorer ---
    try:
        print("--- Executando scraping do Funds Explorer ---")
        executar_scraping_fii_explorer(pasta_destino)
        print("--- Scraping do Funds Explorer Concluído! ---\n")
    except Exception as e:
        print(f"❌ Erro ao executar o scraping do Funds Explorer: {e}\n")

    # --- Sub-módulo 5.3: Executar o scraping do Investing.com ---
    try:
        print("--- Executando scraping do Investing.com ---")
        executar_scraping_fii_investing(pasta_destino)
        print("--- Scraping do Investing.com Concluído! ---\n")
    except Exception as e:
        print(f"❌ Erro ao executar o scraping do Investing.com: {e}\n")

    print("--- Módulo 5 Concluído! ---\n")


def main_standalone():
    """
    Função para execução autônoma. Usa argumento de linha de comando
    ou cria uma pasta padrão automaticamente.
    """
    print("🚀 Iniciando o processo de Web Scraping (Execução Autônoma).")

    # Usa argumento de linha de comando ou caminho padrão
    caminho = sys.argv[1] if len(sys.argv) > 1 else None
    pasta_destino = selecionar_pasta_destino(caminho)

    executar_web_scraping(pasta_destino)


if __name__ == "__main__":
    main_standalone()
