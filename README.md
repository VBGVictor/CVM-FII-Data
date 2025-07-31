# Scrapping_FII_CVM - Análise de Dados

## 📝 Descrição do Projeto

Este repositório contém a análise de dados desenvolvida para o a extração, modelagem e geração de csv's com o objetivo de atingir as demandas exigidas da melhor forma possível e objetivamente para uma montagem de Dashboards interativos para insinghts dos dados publicos disponíveis na CVM sobre informações fundamentalistas de fundos de investimento. Além disso, esta aplicação esta conectada ao GitActions, onde a atualização é feita automaticamente todos os dias as 00:00 executando o programa, apenas com exeção da aplicação FFI_Investing.py que exige atuação manual. 

## 📂 Estrutura de Arquivos

O projeto está organizado da seguinte forma, facilitando a navegação e o entendimento:

```
Scrapping_FII_CVM/
│
├── 📄 app.py         # Notebook principal para execução de todos os notebooks e salva todos na pasta output do projeto.
├── output/         # Pasta onde estaram todas as planilhas atualizadas até o momento.
├── 📄 app_Scrapping.py         # Notebook que executa as aplicações de extração FII_Explorer.py e FII_Investing.py.
├── 📄 ETL_Inicial.py         # Notebook para extração, modelagem dos arquivos CVM.
├── 📄 Dados_Financeiros.py         # Notebook que extrai das planilhas um csv unificado com dados financeiros já coletados pela fase inicial.
├── 📄 Dados_Qualitativos.py         # Notebook que extrai das planilhas um csv unificado com dados qualitativos já coletados pela fase inicial.
├── 📄 Dados_Portifolio.py         # Notebook que extrai das planilhas um csv unificado com dados portifólio já coletados pela fase inicial.
├── 📄 FII_Explorer.py         # Notebook que extrai e organiza 10 FII's de acordo com a liquidez e dividend yield do ranking localizado no site explorer.com.br. Inicialmente desenvolvido para extraidados para uso posterior em dashboards.
├── 📄 FII_Investing.py         # Notebook que extrai e organiza 3 FII's de acordo com as datas de pagamento dos dividendos do site investing.com. Inicialmente desenvolvido para extraidados para uso posterior em dashboards.
├── 📄 IPCAxCDI.py         # Notebook que extrai e organiza os dados de IPCA e CDI para um csv de uso para acompanhamento ou uso posterior em dashboards.

└── 📖 README.md                  # Este arquivo de documentação.
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


## ✍️ Autor

-   **[Victor Barbosa Goveia]**
-   **Contato:** victor.barbosa.gov@gmail.com
-   **LinkedIn:** https://www.linkedin.com/in/victor-barbosa-gov/


