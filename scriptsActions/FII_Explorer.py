import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from tkinter import filedialog, Tk # Tk e filedialog são usados apenas para execução autônoma
import time
import yfinance as yf

# 🛠️ Função de limpeza numérica
def limpar_num(val):
    try:
        val = str(val).replace('.', '').replace(',', '.').replace('%', '').strip()
        return round(float(val), 2)
    except:
        return None

def info_dividendos(ticker, meses=12):
    try:
        yf_ticker = yf.Ticker(ticker)
        hoje = datetime.today()
        inicio = hoje - timedelta(days=meses*30)
        divs = yf_ticker.dividends

        if divs.empty:
            return 0, None, None, None, None

        # Filtra dividendos dos últimos 'meses'
        divs = divs[divs.index >= inicio]
        qtd_pagamentos = len(divs)
        if qtd_pagamentos == 0:
            return 0, None, None, None, None

        primeira_data = divs.index.min().strftime('%Y-%m-%d')
        ultimo_data = divs.index.max().strftime('%Y-%m-%d')
        primeiro_valor = round(divs.min(), 4)
        ultimo_valor = round(divs.max(), 4)

        return qtd_pagamentos, primeira_data, primeiro_valor, ultimo_data, ultimo_valor
    except Exception:
        return 0, None, None, None, None

def executar_scraping_fii_explorer(pasta_destino: Path):
    """
    Executa o scraping de FIIs do site Funds Explorer, processa os dados
    e salva um CSV com o top 10 de dividendos na pasta de destino.
    """
    # 🧭 Configura o Chrome headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')

    # 🚀 Inicia o navegador com WebDriver Manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.fundsexplorer.com.br/ranking")

    print("⏳ Carregando tabela do Funds Explorer...")
    time.sleep(10)  # tempo para garantir que JS carregue

    # 📥 Captura a tabela
    html_tabela = driver.find_element(By.TAG_NAME, 'table').get_attribute('outerHTML')
    driver.quit()

    df = pd.read_html(StringIO(html_tabela))[0]
    print("📌 Colunas capturadas:", df.columns.tolist())

    # 🔁 Renomeia colunas se existirem
    mapa_renomeio = {
        'Fundos': 'codigo_fii',
        'Setor': 'setor',
        'Preço Atual (R$)': 'preco_atual',
        'Dividend Yield': 'dy_12m',
        'Liquidez Diária (R$)': 'liquidez_diaria'
    }
    df.rename(columns={k: v for k, v in mapa_renomeio.items() if k in df.columns}, inplace=True)

    # 🎯 Aplica limpeza apenas nas colunas que existem
    for col in ['preco_atual', 'dy_12m', 'liquidez_diaria']:
        if col in df.columns:
            df[col] = df[col].apply(limpar_num)

    # 📆 Adiciona data de coleta
    df['data_coleta'] = datetime.today().strftime('%Y-%m-%d')

    # 📊 Filtra fundos com liquidez >= 100000
    df_validos = df[df['liquidez_diaria'].fillna(0) >= 100000] if 'liquidez_diaria' in df.columns else df.copy()

    # Lista para armazenar infos adicionais
    infos_dividendos = []

    print("⏳ Consultando histórico de dividendos dos fundos válidos...")

    for codigo in df_validos['codigo_fii']:
        ticker_yf = f"{codigo}.SA"
        info = info_dividendos(ticker_yf, meses=12)
        infos_dividendos.append(info)

    # Cria colunas no df_validos
    df_validos['qtd_pagamentos_12m'] = [info[0] for info in infos_dividendos]
    df_validos['primeira_data_pagamento_12m'] = [info[1] for info in infos_dividendos]
    df_validos['primeiro_valor_pagamento_12m'] = [info[2] for info in infos_dividendos]
    df_validos['ultima_data_pagamento_12m'] = [info[3] for info in infos_dividendos]
    df_validos['ultimo_valor_pagamento_12m'] = [info[4] for info in infos_dividendos]

    # Ordena pelo maior Dividend Yield (dy_12m)
    top_dividendos = df_validos.sort_values(by='dy_12m', ascending=False).head(10)

    # Salva arquivo CSV com todas as informações
    caminho_saida = pasta_destino / 'top10_dividendos_fii_com_pagamentos.csv'
    top_dividendos.to_csv(caminho_saida, sep=';', index=False, decimal=',')

    print(f"✅ Arquivo salvo em: {caminho_saida}")

if __name__ == '__main__':
    # Bloco para permitir a execução autônoma do script para testes
    print("Executando FII_Explorer.py de forma autônoma...")
    root = Tk()
    root.withdraw()
    pasta_selecionada = Path(filedialog.askdirectory(title="Escolha onde salvar o arquivo"))
    
    if pasta_selecionada:
        executar_scraping_fii_explorer(pasta_selecionada)
    else:
        print("❌ Nenhuma pasta selecionada. O programa será encerrado.")
