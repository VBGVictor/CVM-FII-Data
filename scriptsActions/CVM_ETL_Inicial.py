import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import zipfile
import os
from datetime import datetime

URL = "https://dados.cvm.gov.br/dados/FII/DOC/INF_TRIMESTRAL/DADOS/"

def baixar_e_extrair_arquivos(base):
    print(f"Acessando {URL}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    resposta = requests.get(URL, headers=headers)
    if resposta.status_code != 200:
        print(f"Erro ao acessar o site da CVM. Status: {resposta.status_code}")
        return

    soup = BeautifulSoup(resposta.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]

    if not links:
        print("Nenhum arquivo ZIP encontrado.")
        return

    for nome_arquivo in links:
        url_arquivo = urljoin(URL, nome_arquivo)
        nome_limpo = nome_arquivo.replace('.zip', '')
        pasta_destino = base / nome_limpo
        pasta_destino.mkdir(parents=True, exist_ok=True)
        caminho_arquivo = pasta_destino / nome_arquivo

        head = requests.head(url_arquivo, headers=headers)
        if 'Last-Modified' in head.headers:
            data_site = datetime.strptime(head.headers['Last-Modified'], "%a, %d %b %Y %H:%M:%S %Z")
        else:
            data_site = None

        baixar = False
        if not caminho_arquivo.exists():
            print(f"Novo arquivo: {nome_arquivo}")
            baixar = True
        elif data_site:
            data_local = datetime.fromtimestamp(caminho_arquivo.stat().st_mtime)
            if data_site > data_local:
                print(f"Arquivo atualizado: {nome_arquivo}")
                baixar = True
            else:
                print(f"Já atualizado: {nome_arquivo}")
        else:
            print(f"Não foi possível comparar data. Pulando: {nome_arquivo}")

        if baixar:
            try:
                with requests.get(url_arquivo, stream=True) as r:
                    r.raise_for_status()
                    with open(caminho_arquivo, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                if data_site:
                    os.utime(caminho_arquivo, (data_site.timestamp(), data_site.timestamp()))
                print(f"Baixado: {nome_arquivo}")

                with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                    zip_ref.extractall(pasta_destino)
                print(f"Extraído: {nome_arquivo}")

            except Exception as e:
                print(f"Erro ao baixar {nome_arquivo}: {e}")

def executar_download_cvm(pasta_dados_cvm: Path):
    """
    Função principal para orquestrar o download e extração dos arquivos da CVM.
    Recebe o caminho da pasta como argumento.
    """
    print("--- Módulo 1: Download e Extração de Dados da CVM ---")
    pasta_dados_cvm.mkdir(parents=True, exist_ok=True)
    baixar_e_extrair_arquivos(pasta_dados_cvm)
    print("--- Módulo 1 Concluído! ---\n")