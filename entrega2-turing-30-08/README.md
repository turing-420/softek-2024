
## Dashboard de Demandas

Este projeto visa fornecer uma visualização interativa e abrangente das demandas de um Service Desk e AMS nível 2, utilizando dados históricos para análise de desempenho e otimização de recursos.

### Demonstração Online

Você pode acessar o dashboard de demandas diretamente através do link: 
[https://dashboardsofttek.vercel.app/](https://dashboardsofttek.vercel.app/)

### Como Executar o Projeto

#### 1. Executar o Front-End

Para visualizar o dashboard de demandas, você pode usar uma das seguintes opções:

1. **Usando Node.js (http-server)**:
   - Com Node.js instalado, abra o terminal ou prompt de comando.
   - Na raiz do projeto, execute o comando:
     ```bash
     npm start
     ```
   - Abra o navegador e vá para:
      [http://127.0.0.1:8000](http://127.0.0.1:8000)


2. **Usando Live Server (VS Code)**:
   - Abra o Visual Studio Code e navegue até a pasta `frontend`.
   - Clique com o botão direito no arquivo `index.html` e selecione "Open with Live Server".
   - O navegador abrirá automaticamente o dashboard em execução.


#### 2. Executar os Notebooks

Os notebooks Jupyter localizados na pasta `backend/softtek/main` podem ser executados para preparação e análise de dados:

1. Certifique-se de que o Jupyter Notebook esteja instalado:
   ```bash
   pip install notebook
   ```
2. Navegue até a pasta do projeto:
   ```bash
   cd caminho/para/o/diretorio/backend/softtek/main
   ```
3. Inicie o Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
4. Abra e execute os notebooks na seguinte ordem:
   - `Indicador/001_dataprep.ipynb`: Preparação de dados.
   - `Indicador/002_ETL_Indicadores.ipynb`: Processo de ETL.
   - `model_e_distribuidor/001_EDA.ipynb`: Análise exploratória dos dados.
   - `model_e_distribuidor/002_preditivo_.ipynb`: Modelagem preditiva.
   - `model_e_distribuidor/003_distribuidor.ipynb`: Distribuição dos resultados.


### Estrutura de Arquivos e Pastas

```
/final
├── Arquitetura.png
├── backend
│   └── softtek
│       ├── db_softtek
│       │   ├── cubo_anl
│       │   └── modelo
│       ├── Instruções de funcionamento.txt
│       └── main
│           ├── Indicador
│           │   ├── 001_dataprep.ipynb
│           │   └── 002_ETL_Indicadores.ipynb
│           ├── instalacao_bibliotecas.ipynb
│           └── model_e_distribuidor
│               ├── 001_EDA.ipynb
│               ├── 002_preditivo_.ipynb
│               └── 003_distribuidor.ipynb
├── DB_Modelagem.png
├── frontend
│   ├── assets
│   ├── data
│   ├── index.html
│   ├── scripts.js
│   └── sobre.html
├── Projeto.pdf
└── README.md
```

### Front-End

```
frontend/index.html: Página principal do dashboard de demandas.
frontend/sobre.html: Página "Sobre o Projeto" com informações da equipe.
frontend/styles.css: Estilos utilizados nas páginas HTML.
frontend/assets: Pasta com imagens e outros arquivos de mídia.
frontend/data: Pasta que contém arquivos de dados JSON para alimentar o dashboard.
```

### Back-End

```
backend/softtek: Contém scripts de back-end e notebooks Jupyter para preparação de dados e modelagem.
Indicador: Notebooks para pré-processamento e ETL de indicadores.
model_e_distribuidor: Notebooks para análise exploratória de dados, modelagem preditiva e distribuição.
```

### Documentação e Arquitetura

```
Arquitetura.png: Diagrama da arquitetura do sistema.
DB_Modelagem.png: Diagrama Entidade-Relacionamento (ER) do banco de dados.
Projeto.pdf: Documento com detalhes do projeto, incluindo descrição da solução e diagramas.
```

### Conclusão

Neste projeto, desenvolvemos um dashboard de demandas que fornece uma visualização interativa e abrangente das demandas do Service Desk e AMS nível 2. Utilizando dados históricos, o dashboard permite a análise de desempenho e otimização de recursos.

A estrutura de arquivos e pastas do projeto está organizada de forma clara, facilitando a navegação e localização dos arquivos relevantes. 

O front-end consiste em páginas HTML, estilos CSS e arquivos de dados JSON para alimentar o dashboard. 

Já o back-end inclui scripts e notebooks Jupyter para a preparação de dados e modelagem.

A documentação e arquitetura do projeto estão disponíveis nos arquivos `Arquitetura.png`, `DB_Modelagem.png` e `Projeto.pdf`. Esses arquivos fornecem detalhes sobre a arquitetura do sistema, o diagrama Entidade-Relacionamento do banco de dados e uma descrição completa da solução.

Em resumo, este projeto oferece uma solução completa para a visualização e análise de demandas de um Service Desk e AMS nível 2. 

Com o dashboard de demandas, é possível tomar decisões mais informadas e otimizar o uso de recursos.