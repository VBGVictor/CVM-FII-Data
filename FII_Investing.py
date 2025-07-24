from pathlib import Path
from tkinter import filedialog
from tkinter import Tk # Usado apenas para execução autônoma
import pandas as pd
from playwright.sync_api import sync_playwright

tickers_investing = {
    "HGLG11": "fii-cshg-log-dividends",
    "RCRB11": "fii-riob-rc-dividends",
    "HGPO11": "cshg-jhsf-prime-offices-dividends",
    "FGAA11": "fg-agro-fi-cad-agroind-fiagro-imob-dividends",
    "HCRI11": "fii-hospital-da-crianca-dividends",
    "HGBS11": "cshg-brasil-shopping-dividends",
    "HGRU11": "cshg-renda-urbana-fii-dividends",
    "VISC11": "vinci-shopping-centers-fii-dividends",
}

def obter_dividendos_investing(slug, ticker_label):
    url = f"https://www.investing.com/equities/{slug}"
    dados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            try:
                page.locator("text=Accept All").click(timeout=3000)
            except:
                pass

            page.wait_for_selector("table.freeze-column-w-1", timeout=20000)

            rows = page.query_selector_all("table.freeze-column-w-1 tbody tr")
            for row in rows:
                cols = row.query_selector_all("td")
                if len(cols) >= 5:
                    data_ex = cols[0].inner_text().strip()
                    dividendo = cols[1].inner_text().strip()
                    tipo = cols[2].inner_text().strip()
                    data_pagamento = cols[3].inner_text().strip()
                    yield_ = cols[4].inner_text().strip()
                    dados.append({
                        "Ticker": ticker_label.upper(),
                        "Data Ex": data_ex,
                        "Dividendo": dividendo,
                        "Tipo": tipo,
                        "Data Pagamento": data_pagamento,
                        "Yield": yield_
                    })
        except Exception as e:
            print(f"⚠️ Erro ao buscar {ticker_label.upper()}: {e}")
        finally:
            browser.close()

    return dados

def executar_scraping_fii_investing(pasta_destino: Path):
    """
    Executa o scraping de dividendos de FIIs do site Investing.com
    e salva um CSV consolidado na pasta de destino.
    """
    # Coleta para todos os FIIs
    todos_dados = []
    for ticker, slug in tickers_investing.items():
        print(f"🔍 Coletando dividendos de {ticker.upper()}...")
        dados = obter_dividendos_investing(slug, ticker)
        todos_dados.extend(dados)

    df_res = pd.DataFrame(todos_dados)
    caminho_saida = pasta_destino / "datas_pagamento_dividendos.csv"
    df_res.to_csv(caminho_saida, sep=";", index=False)
    print(f"✅ Arquivo salvo com sucesso em: {caminho_saida}")

if __name__ == '__main__':
    # Bloco para permitir a execução autônoma do script para testes
    print("Executando FII_Investing.py de forma autônoma...")
    root = Tk()
    root.withdraw()
    pasta_selecionada = Path(filedialog.askdirectory(title="Escolha onde salvar o arquivo"))
    if pasta_selecionada:
        executar_scraping_fii_investing(pasta_selecionada)
    else:
        print("❌ Nenhuma pasta selecionada. O programa será encerrado.")
