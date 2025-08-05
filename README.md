# CVM-FII-Data - Análise de Dados

## 📝 Descrição do Projeto

Este projeto automatiza a extração, tratamento e disponibilização de dados de Fundos Imobiliários (FIIs) da CVM e de portais financeiros como Investing.com e FundsExplorer. A aplicação inclui rotinas de ETL via GitActions, integração uma API Flask para acesso local dos dados já processados para disponibilidades para analises de dados, verificações por outras API's e futuro desenvolvimento proprio de analises de ML. 

## 📂 Estrutura de Arquivos

O projeto está organizado da seguinte forma, facilitando a navegação e o entendimento:

```
CVM-FII-Data/
│
├── app/                              # Aplicação Flask para disponibilização local dos dados
│   ├── __init__.py
│   ├── routes/
│   │   └── fii.py                    # Rotas para visualização e listagem de arquivos
│   ├── servicer/
│   │   └── fii_data.py              # Serviço para leitura dos arquivos e organização dos dados
│   └── templates/                   # Templates HTML
│       ├── index.html
│       ├── table.html
│       ├── ver_arquivo.html
│       └── visualizar.html
│
├── scriptActions/                   # Notebooks para extração e tratamento dos dados
│   ├── app.py                       # Executa todos os notebooks da pipeline
│   ├── app_Scrapping.py            # Integra FII_Explorer e FII_Investing
│   ├── ETL_Inicial.py              # Coleta e trata arquivos da CVM
│   ├── Dados_Financeiros.py        # Extrai e organiza dados financeiros dos FIIs
│   ├── Dados_Qualitativos.py       # Extrai e organiza dados qualitativos
│   ├── Dados_Portifolio.py         # Extrai e organiza dados de portfólio
│   ├── FII_Explorer.py             # Ranking de FIIs do site FundsExplorer
│   ├── FII_Investing.py            # Datas de pagamento de dividendos via Investing.com
│   ├── IPCAxCDI.py                 # Dados históricos de inflação e taxa CDI
│   └── requirements.txt            # Requisitos para GitHub Actions
│
├── output/dados_projeto             # Arquivos CSV prontos para análise
│   └── ...                          # Todos os arquivos tratados (e originais) da pipeline

├── requirements.txt                 # Dependências para rodar a API Flask
├── run.py                           # Arquivo principal para iniciar a API Flask
└── README.md                        # Documentação do projeto

```

## 🚀 Como Executar o Projeto

### Passo a passo

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/Scrapping_FII_CVM.git
cd Scrapping_FII_CVM
```
2. **(Opicional) Crie um ambiente virtual**

```bash
python -m venv venv
source venv/Scripts/activate #Windowns
source venv/bin/activate #Linux
```
3. **Instalar dependências da API Flask**

```bash
pip install -r requirements.txt
```
4. **Rodar a API local**

```bash
python run.py
```

## ✍️ Autor

-   **[Victor Barbosa Goveia]**
-   **Contato:** victor.barbosa.gov@gmail.com
-   **LinkedIn:** https://www.linkedin.com/in/victor-barbosa-gov/


