# Temperature Watcher API

Esta API foi criada para ser utilizada em um projeto da faculdade durante o 6º semestre de Eng. de Automação e Controle, sendo também, minha primeira API criada para utilizar em um projeto real.

A ideia deste projeto é monitorar uma variável de processo, armazenar dados referentes a ela, permitir a visualização desses dados e a alteração de parâmetros para gerar comportamentos diferentes no sistema.<br>
As variáveis de processo escolhidas foram temperatura e humidade, então com um sensor conectado a um Arduino coletamos essas informações. Através da comunicação Serial do microcontrolador enviamos os dados para o computador, onde um programa Python faz o monitoramento da Porta Serial para receber os dados, além disso, esse programa também faz requisições a API para salvar os dados coletados.<br>
Por sua vez, com um aplicativo de celular é possível visualizar os dados através de um gráfico, navegar por um histórico e alterar o parâmetro de controle da variável de processo.

O parâmetro de controle é um valor determinado pelo usuário para manter a temperatura. Ao definir um novo valor para ele, o usuário determina a temperatura no qual quer manter controlada. Este controle é feito através da detecção do sensor comparada ao valor definido pelo usuário e caso haja a necessidade de gerar calor, uma lâmpada com filamento é acessa próxima ao sistema, caso contrário, a lâmpada se mantém apagada. 

### Tecnologias usadas:

As tecnologias usadas para essa aplicação foram:

* **Flask**
* **Heroku**
* **MySQL**

<div style="text-align: center;">
    <img src="https://seeklogo.com/images/F/flask-logo-44C507ABB7-seeklogo.com.png" width="8%" style="margin-right: 40px;">
    <img src="https://image.flaticon.com/icons/png/512/873/873120.png" width="10%" style="margin-right: 40px;">
    <img src="https://cdn.iconscout.com/icon/free/png-512/mysql-19-1174939.png" width="12%">
</div>

### Estrutura dos arquivos:

O código para executação dos processos lógicos, comunicações com o banco de dados e para fazer as configurações da API foi dividido em 3 arquivos:
* **_Database.py_:** Arquivo responsável por executar as queries do banco de dados;
* **_Tools.py_:** Arquivo responsável por trabalhar funções lógicas que são usadas mais de uma vez na aplicação;
* **_app.py_:** Arquivo de configuração da API, contendo chamadas as variáveis de ambiente para configurar o banco de dados, definindo as rotas e a execução da aplicação.

### Rotas (Endpoits):

Esta aplicação possuí 3 rotas, sendo elas:
* **_/graphdata_:** Possuí apenas o método GET habilitado e é utilizado para puxar as informações do banco de dados armazenadas com o uso do sensor;
* **_/temperaturecontroller_:** Possuí os métodos GET e POST habilitados e é utilizado para configurar ou puxar as informações usadas pelo controlador de temperatura (parâmetros de controle);
* **_/search_:** Possuí apenas o método GET habilitado e é utilizado para coletar as informações filtradas de acordo com um período de tempo no banco de dados.
