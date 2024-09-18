
## Dashboard

Este projeto visa fornecer uma visualização interativa e abrangente das demandas de um Service Desk e AMS nível 2, utilizando dados históricos para análise de desempenho e otimização de recursos.

### Demonstração Online

Você pode acessar o dashboard diretamente através do link: 
[https://dashboardsofttek.vercel.app/](https://dashboardsofttek.vercel.app/)

### Como Executar o Projeto

#### 1. Executar o Front-End

Para visualizar o dashboard, você pode usar uma das seguintes opções:

1. **Usando Node.js (live-server)**:
   - Certifique-se de que o Node.js está instalado.
   
   - Com Node.js instalado, abra o terminal ou prompt de comando.

   - Instale o pacote live-server:
     ```bash
     npm install live-server
     ```
   - Na raiz do projeto, execute o comando:
     ```bash
     npm start
     ```
   - Abra o navegador e vá para:
      [http://127.0.0.1:8080](http://127.0.0.1:8080)


2. **Usando Live Server (VS Code)**:
   - Clique com o botão direito no arquivo `index.html` e selecione "Open with Live Server".
   - O navegador abrirá automaticamente o dashboard em execução.


#### 2. Executar os Notebooks

Os notebooks Jupyter localizados na pasta `backend/softtek/main` podem ser executados para preparação e análise de dados:

Siga as `Instruções de funcionamento.txt`

### Documentação e Arquitetura

```
Arquitetura.png: Diagrama da arquitetura do sistema.
DB_Modelagem.png: Diagrama Entidade-Relacionamento (ER) do banco de dados.
Projeto.pdf: Documento com detalhes do projeto, incluindo descrição da solução e diagramas.
```

### Conclusão

Oferecemos uma solução completa para a visualização e análise de um Service Desk e AMS nível 2. 

Com o dashboard, é possível tomar decisões mais informadas e otimizar o uso de recursos.

Front-end consiste em páginas HTML, estilos CSS e arquivos de dados JSON para alimentar o dashboard. 

Back-end inclui scripts e notebooks Jupyter para a preparação de dados e modelagem.

A documentação e arquitetura do projeto estão disponíveis nos arquivos `Arquitetura.png`, `DB_Modelagem.png` e `Projeto.pdf`. Esses arquivos fornecem detalhes sobre a arquitetura do sistema, o diagrama Entidade-Relacionamento do banco de dados e uma descrição completa da solução.
