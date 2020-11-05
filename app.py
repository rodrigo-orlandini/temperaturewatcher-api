import os
from flask import Flask, request        #Trazendo Flask e request do módulo Flask para trabalhar as rotas
from flask_cors import CORS
from Database import Database         #Importando classe para trabalhar com o DB
from Tools import Tools               #Importando classe utilitária

#Constantes para configurar a conexão com o banco de dados
HOST = 'db4free.net'
USER = 'rodrigotest'
PASSWORD = 'knameenter22'
DATABASE = 'tempwatchertest'

#Inicializando as configurações da aplicação
application = Flask(__name__)

cors = CORS(application, resource={r"/*": {"origins": "*"} })

#Rota para coletar as informações do gráfico
@application.route("/graphdata", methods=['GET'])
def getGraphData():
  databaseConnection = Database(HOST, USER, PASSWORD, DATABASE)     #Configurando conexão com o Banco de Dados
  responseDatabase = databaseConnection.selectTemperatureHumidityData(limit=10)    #Coletando resposta da query executada no DB
  fields = ["id", "temperature", "humidity", "datetime"]          #Campos para o dicionário de resposta

  #Utilizando o padrão de Dicionário para as respostas do DB
  response = Tools.extractResponse(responseDatabase, fields)
  #Se ocorrer algum possível erro, retorna essa mensagem
  if not response:
    return Tools.showResponse(500, "Internal Server Error")

  #Retorna a resposta de sucesso e o JSON com as informações
  return Tools.showResponse(200, "Successfully", title="data", content=response)


#Rota para configurar ou pegar as informações do controlador de temperatura
@application.route("/temperaturecontroller", methods=["GET", "POST"])
def temperatureControllerHandler():

  databaseConnection = Database(HOST, USER, PASSWORD, DATABASE)       #Configurando conexão com o Banco de Dados

  #Verifica qual o método da requisição
  if request.method == "GET":
    #Sendo GET, a última informação do registro do controlador de temperatura é puxado do DB
    responseDatabase = databaseConnection.selectTemperatureController()
    fields = ["id", "temperature", "status"]          #Campos para o dicionário de resposta

    #Utilizando o padrão de Dicionário para as respostas do DB
    response = Tools.extractResponse(responseDatabase, fields)
    #Se ocorrer algum possível erro, retorna essa mensagem
    if not response:
      return Tools.showResponse(500, "Internal Server Error")

    #Retorna a resposta de sucesso e o JSON com as informações
    return Tools.showResponse(200, "Successfully", title="controller", content=response)

  elif request.method == "POST":
    #Sendo POST, é pego o corpo da requisição
    body = request.get_json()

    #Faz a validação da existência do valor temperature dentro do corpo da requisição
    if 'temperature' not in body:
      return Tools.showResponse(400, "'temperature' argument is requested")
    
    try:
      #Faz o arredondamento do valor da temperatura e converte ela para int
      body["temperature"] = int(round(body["temperature"]))
      #Verifica se a temperatura está dentro dos limites 0 á 50
      if 0 > body["temperature"] > 50:
        return Tools.showResponse(400, "'temperature' argument must be an number between 0 and 50")
    except:
      return Tools.showResponse(400, "'temperature' argument must be an number between 0 and 50")

    try:
      #Valida a existência do valor status dentro do corpo da requisição
      if 'status' in body:
        #Valida o valor de status, que deve ser somente 0 ou 1 e faz o INSERT na tabela de controllers
        if body["status"] == 0 or body["status"] == 1:
          databaseConnection.insertTemperatureController(body['temperature'], status=body['status'])
        else:
          return Tools.showResponse(400, "'status' argument must be 0 or 1")
      else:
        databaseConnection.insertTemperatureController(body['temperature'])
    except:
      #Se ocorrer algum possível erro, retorna essa mensagem
      return Tools.showResponse(500, "Internal Server Error")

    #Retorna a resposta de sucesso e o JSON com as informações
    return Tools.showResponse(200, "Successfully")


#Rota para coletar informações para a filtragem
@application.route("/search", methods=["GET"])
def getFilterData():
  #Pega os valores de inicio e do fim que serão aplicados no filtro passados pela URL (Query Parameters)
  startDate = request.args.get("start")
  endDate = request.args.get("end")
 
  #Passam por uma validação de data
  if not Tools.dateValidator(startDate):
    return Tools.showResponse(400, "'start' argument must be a date yyyy-mm-dd")
  if endDate == "" and not Tools.dateValidator(endDate):
    return Tools.showResponse(400, "'end' argument must be a date yyyy-mm-dd")

  databaseConnection = Database(HOST, USER, PASSWORD, DATABASE)     #Configurando conexão com o Banco de Dados
  responseDatabase = databaseConnection.selectFilteredData(startDate, endDate)    #Faz um select no DB aplicando os valores dos filtros
  fields = ["id", "temperature", "humidity", "datetime"]          #Campos para o dicionário de resposta

  #Utilizando o padrão de Dicionário para as respostas do DB
  response = Tools.extractResponse(responseDatabase, fields)
  #Se ocorrer algum possível erro, retorna essa mensagem
  if not response:
    return Tools.showResponse(500, "Internal Server Error")

  #Retorna a resposta de sucesso e o JSON com as informações
  return Tools.showResponse(200, "Successfully", title='data', content=response)


def main():
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
