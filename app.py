import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import sys
from CVM_ETL_Inicial import executar_download_cvm
from CVM_Dados_Financeiros import executar_consolidacao_financeira
from CVM_Dados_Qualitativos import executar_consolidacao_qualitativa
from CVM_Dados_Portifolio import executar_consolidacao_portfolio
from app_Scraping import executar_web_scraping

def selecionar_pasta_dados():
    """
    Abre uma janela para o usuário selecionar a pasta principal 
    onde os dados serão lidos e salvos.
    """
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.askdirectory(
        title="Selecione a Pasta Principal para Leitura e Gravação dos Dados"
    )
    if not caminho:
        print("❌ Nenhuma pasta selecionada. O programa será encerrado.")
        sys.exit()
    return Path(caminho)

def main():
    """
    Função principal que orquestra a execução de todos os scripts do projeto.
    """
    print("🚀 Iniciando o processo de ETL/ELT para dados de FIIs.")
    print("="*60)

    # --- Passo 1: Seleção centralizada das pastas ---
    pasta_dados_cvm = selecionar_pasta_dados()
    print(f"📁 Pasta de dados selecionada: {pasta_dados_cvm}\n")

    # --- Passo 2: Executar o script de download e extração da CVM ---
    executar_download_cvm(pasta_dados_cvm)

    # --- Passo 3: Consolidar dados financeiros ---
    executar_consolidacao_financeira(pasta_dados_cvm)

    # --- Passo 4: Consolidar dados qualitativos ---
    executar_consolidacao_qualitativa(pasta_dados_cvm)

    # --- Passo 5: Consolidar dados de portfólio ---
    executar_consolidacao_portfolio(pasta_dados_cvm)

    # --- Passo 6: Executar Web Scraping ---
    executar_web_scraping(pasta_dados_cvm)

    print("="*60)
    print("✅ Processo finalizado com sucesso!")

if __name__ == "__main__":
    main()
