import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import sys

# Importa as funções principais dos outros scripts.
# É crucial que os arquivos FII_Explorer.py e FII_Investing.py
# estejam na mesma pasta e sejam ajustados para exportar estas funções.
from FII_Explorer import executar_scraping_fii_explorer
from FII_Investing import executar_scraping_fii_investing
from IPCAxCDI import executar_coleta_indicadores

def selecionar_pasta_destino():
    """
    Abre uma janela para o usuário selecionar a pasta de destino
    onde os arquivos de scraping serão salvos.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter
    caminho = filedialog.askdirectory(
        title="Selecione a Pasta para Salvar os Arquivos de Scraping"
    )
    if not caminho:
        print("❌ Nenhuma pasta selecionada. O programa será encerrado.")
        sys.exit()
    return Path(caminho)

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
    """Função para executar este script de forma autônoma para testes."""
    print("🚀 Iniciando o processo de Web Scraping (Execução Autônoma).")
    pasta = selecionar_pasta_destino()
    executar_web_scraping(pasta)

if __name__ == "__main__":
    main_standalone()
