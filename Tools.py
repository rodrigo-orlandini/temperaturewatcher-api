import datetime         #Importando datetime para trabalhar com datas

class Tools:

  #Método estático para validar a data para ser salva no DB
  @staticmethod
  def dateValidator(date):
    #Tenta fazer a conversão da string para formato de data
    try:
      datetime.datetime.strptime(date, '%Y-%m-%d')
      return True
    #Caso não tiver o formato necessário retorna um erro
    except ValueError:
      return False


  #Método estático para ajustar a resposta em um formato padrão
  @staticmethod
  def showResponse(status, message, title=False, content=False):
    response = {}
    response['status'] = status
    response['message'] = message

    if title and content:
      response[title] = content

    return response

  #Método estático para converter os dados em um padrão Dicionário (JSON)
  @staticmethod
  def extractResponse(data, fields):
    response = {}
    register = 0

    #Validação do fields passado como parâmetro
    length = len(fields)
    if str(type(fields)) != "<class 'list'>" or length == 0: 
      return False
    if any(str(type(element)) != "<class 'str'>" for element in fields):
      return False

    try:
      #For para organizar a estrutura JSON que será devolvida na response
      for element in data:
        register = 'register%s'%(element[0])
        response[register] = {}
        for i in range(length):
          response[register][fields[i]] = element[i]
      return response
    except:
      #Se ocorrer algum possível erro, retorna essa mensagem
      return False