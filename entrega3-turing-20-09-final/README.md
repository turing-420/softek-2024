
## Dashboard

Este projeto visa fornecer uma visualização interativa e abrangente das demandas de um Service Desk e AMS nível 2, utilizando dados históricos para análise de desempenho e otimização de recursos.

### 📈 DEMO ONLINE 📊 ###

Você pode acessar o dashboard diretamente através do link: 
[https://dashboardsofttek.vercel.app/](https://dashboardsofttek.vercel.app/)

### Como Executar o Projeto

Escolha a melhor opção para você:
- Docker (recomendado)
- Nodejs + live-server (npm start)
- VS Code / Jupyter


### Docker 🐳
        - Você pode rodar o docker-compose para executar o front-end + ETL processando o `backend/softtek/db_softtek/FIAP_DataBase_v1.xlsx`
            ```
            docker-compose build
            docker-compose up
            ```
        - Apenas o front-end:
            ```
            docker build -t dashboard .
            docker run -p 80:80 dashboard
            ```
        - Apenas o ETL no arquivo `db_softtek/FIAP_DataBase_v1.xlsx`:
            ```
            cd backend/softtek
            docker build -t backend .
            docker run -v $(pwd)/db_softtek:/app/db_softtek -v $(pwd)../../../data:/data backend
            ```


### Executar o Front-End 🖌

Para visualizar o dashboard, siga uma das opções abaixo:

    1. **Node.js (live-server)**:
        - Certifique-se de que o Node.js está instalado.
        - No terminal, navegue até a pasta raiz do projeto e execute o seguinte comando:
            ```
            npm run start
            ```
        - Abra o navegador e acesse o endereço:
            ```
            http://127.0.0.1:8080
            ```

    2. **Live Server (VS Code)**:
        - Abra o projeto no Visual Studio Code.
        - Clique com o botão direito no arquivo `index.html` e selecione "Open with Live Server".
        - O navegador será aberto automaticamente com o dashboard em execução.

    3. **Docker**:
        - Com Docker instalado, rode:
            ```
            docker build -t dashboard .
            docker run -p 80:80 dashboard
            ```

### Executar o Back-End (Notebooks Jupyter) 👩‍💻

Os notebooks Jupyter localizados na pasta `backend/softtek/main` podem ser executados para preparação e análise de dados:

Siga as `Instruções de funcionamento.txt`



### Ferramentas Utilizadas 🔧

- Jupyter Notebook, pandas, matplotlib para o backend e análise de dados.
- HTML5, CSS3, e JavaScript para o desenvolvimento do front-end.
- Chart.js para visualização gráfica dos dados.
- Bootstrap para o design responsivo.
- JSON como formato para os dados.


### Observações

- Para problemas com execução ou dúvidas técnicas, por favor, entre em contato com o grupo.


### Documentação e Arquitetura

```
Arquitetura.png: Diagrama da arquitetura do sistema.
DB_Modelagem.png: Diagrama Entidade-Relacionamento (ER) do banco de dados.
Projeto.pdf: Documento com detalhes do projeto, incluindo descrição da solução e diagramas.
```

### Conclusão

Oferecemos uma solução completa para a visualização e análise de um Service Desk e AMS nível 2. 

Com o dashboard, é possível tomar decisões mais informadas e otimizar o uso de recursos.

Front-end: páginas HTML, estilos CSS e arquivos de dados JSON para alimentar o dashboard. 

Back-end: scripts e notebooks Jupyter para a preparação de dados e modelagem.

A documentação e arquitetura do projeto estão disponíveis nos arquivos `Arquitetura.png`, `DB_Modelagem.png` e `Projeto.pdf`. Esses arquivos fornecem detalhes sobre a arquitetura do sistema, o diagrama Entidade-Relacionamento do banco de dados e uma descrição completa da solução.
