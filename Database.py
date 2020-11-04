import pymysql                #Importando módulo para fazer conexão com o banco de dados

class Database:

  #Método construtor com host (Local onde o banco está hospedado), user (Usuário do banco), password (Senha do
  # banco) e database (Em qual compartimento está sendo armazenado)
  def __init__(self, host, user, password, database):
    self.host = host
    self.user = user
    self.password = password
    self.database = database

  #Função padrão para executar as queries
  def executeQuery(self, query):
    #Abrindo conexão com o banco
    connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
    
    try:
      #Estabelecendo cursor e executando a query no banco
      with connection.cursor() as cursor:
          cursor.execute(query)
          #Coletando resultados (Caso a query for um SELECT)
          result = cursor.fetchall()
      #Registrando as alterações feitas no banco
      connection.commit()
    except:
      #Caso de algum erro no 'try' acima ele levanta a exeção e passa uma mensagem de erro
      result = "error on query execute"
    finally:
      #Após todo o processo, a conexão com o banco é fechada
      connection.close()

    #Retorna o resultado da execução da query
    return result

  #Método para pegar os dados da tabela temp_humidity, podendo ou não ter um limite
  def selectTemperatureHumidityData(self, limit=False):
    
    if limit:
      query = 'SELECT * FROM `temp_humidity` ORDER BY id_register DESC LIMIT %s'%(limit)
    else:
      query = "SELECT * FROM `temp_humidity`"

    response = self.executeQuery(query)
    return response

  #Método para pegar o último registro do controlador de temperatura
  def selectTemperatureController(self):

    query = 'SELECT * FROM `temperature_controller` ORDER BY id_controller DESC LIMIT 1'
    response = self.executeQuery(query)
    return response

  #Método para pegar os valores filtrados por data da tabela temp_humidity
  def selectFilteredData(self, startDate, endDate):

    query = 'SELECT * FROM `temp_humidity` WHERE DATE(date_register) BETWEEN "%s" AND "%s" ORDER BY id_register DESC'%(startDate, endDate)
    response = self.executeQuery(query)
    return response

  #Método para fazer a inserção de novos valores na tabela temperature_controller, onde o padrão de status é ativado
  def insertTemperatureController(self, temperature, status=1):

    query = 'INSERT INTO `temperature_controller` (`value_controller`, `status_controller`) VALUES (%i, %i)'%(temperature, status)
    response = self.executeQuery(query)
    return response
