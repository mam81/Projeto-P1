import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
# extras ~ (data, hora, prioridade, contexto, projeto)
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração.

def adicionar(descricao, extras):
  novaAtividade = ""
  # não é possível adicionar uma atividade já existente. 
  for i in listaOrdenada:
    if (i[0] == descricao) and (i[1] == extras):
      print("ERRO!")
      print("Compromisso já existente no arquivo!")
      return False
  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    print("ERRO!")
    print("Descrição do compromisso obrigatória!")
    return False
  else:
    for indice,i in enumerate(extras):
        if indice == 2:
          if  i != "":
            novaAtividade += i + " " + descricao + " "
          else:
            novaAtividade += descricao + " "
          
        else:
          if i != "":
            novaAtividade += i + " "
  
  # Escreve no TODO_FILE. 
  try:
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return novaAtividade

# Valida a prioridade.
def prioridadeValida(pri):
      if len(pri) == 3:
            if (pri [0] == '(') and (pri[2] == ')'):
                  if (pri[1] >= 'A' and pri[1] <= 'Z') or (pri[1] >= 'a' and pri[1] <= 'z') :
                        return True
      else:
          return False

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.

def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    horas = horaMin[0] + horaMin[1]
    minutos = horaMin[2] + horaMin[3]
    if horas < '0' or horas > '23' or minutos < '0' or minutos > '59' :
      return False
    else:
      return True
    
def find(numero,lista):
  if len(lista) == 0:
    return False
  else:
    head = lista.pop()
    if numero == head:
      return True
    else:
      return find(numero,lista)

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias emr fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto.

def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):
    return False
  else:

    dias = (data[0] + data[1])
    mes = (data[2] + data[3])
    ano = (data[4] + data[5] + data[6] + data[7])
      
    if (dias < '00') or (dias > '31') or (mes < '01' or mes > '12'):
      return False
    else:
      listaMeses31 = ['01','03','05','07','08','10','12']
      listaMeses30 = ['04','06','09','11']

      verificacaoMes = find(mes,listaMeses31[:])
      if verificacaoMes == True:
              diasMaximo = '31'
              if dias > diasMaximo:
                    return False
              else:
                    return True  
      else:
        verificacaoMes = find(mes,listaMeses30[:])
        if verificacaoMes == True:
              diasMaximo = '30'
              if dias > diasMaximo:
                    return False
              else:
                    return True  
        else:
            diasMaximo = '29'
            if dias <= diasMaximo:
                  return True  
            else:
                  return False
  
# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if (len(proj) < 2) or (proj[0] != '+') :
    return False
  else:
    return True
    
# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if (len(cont) < 2) or (cont[0] != '@') :
    return False
  else:
    return True

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True

def verificacaoTrue(funcao,parametro):
    if funcao(parametro) == True:
        return parametro
    else:
      return False
    
# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
# (descrição, prioridade, (data, hora, contexto, projeto))
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.

def concatenacaoListaRecursiva(lista):
  if len(lista) == 0:
    return ""
  elif len(lista) == 1:
    head = lista.pop(0)
    return head + concatenacaoListaRecursiva(lista)
  else:
    head = lista.pop(0)
    return head + " " + concatenacaoListaRecursiva(lista)

def organizar(linhas):      
    itens = []      
    for l in linhas:
      data = '' 
      hora = ''
      pri = ''
      desc = ''
      contexto = ''
      projeto = ''
  
      l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
      listaVariaveis = [data,hora,pri,contexto,projeto]
      listaVerificacoes = [dataValida,horaValida,prioridadeValida,contextoValido,projetoValido]
      i = 0
      while i < len(linhas):
            valor = linhas[i]
            cond = True
            for indice,validacoes in enumerate(listaVerificacoes):
                  if cond == True:
                        if validacoes(valor) == True:
                            listaVariaveis[indice] = valor
                            cond = False
                            linhas.pop(i)
            if cond == True:
                  i += 1
      for indice,i in enumerate(listaVariaveis):
            if i != "":
                  if indice == 0:
                        data += i
                  elif indice == 1:
                        hora += i
                  elif indice == 2:
                        pri += i
                  elif indice == 3:
                        contexto += i
                  else:
                        projeto += i
      desc = concatenacaoListaRecursiva(linhas)
      itens.append((desc, (data, hora, pri, contexto, projeto)))
      
    return itens

# Processa os tokens um a um, verificando se são as partes da atividade.
# Por exemplo, se o primeiro token é uma data válida, deve ser guardado
# na variável data e posteriormente removido a lista de tokens. Feito isso,
# é só repetir o processo verificando se o primeiro token é uma hora. Depois,
# faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
# para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
# corresponde à descrição. É só transformar a lista de tokens em um string e
# construir a tupla com as informações disponíveis. 

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém.
                  
def formatoComparacaoData(data):
    data = int(data[4:] + data[2:4] + data[:2])
    return data
  
def bubbleSortPrioridade(lista):
  for x in lista: 
    atual = 0
    while atual < len(lista) - 1:
      if lista[atual][1][2].upper() > lista[atual+1][1][2].upper():
        temp = lista[atual]
        lista[atual] = lista[atual+1]
        lista[atual+1] = temp
      atual = atual + 1
  return lista

def ordenarPorPrioridade(itens):
      listaAuxiliar = []
      i = 0
      while  i < len(itens):
          if prioridadeValida(itens[i][1][2]) != True:
            listaAuxiliar.append(itens[i])
            itens.pop(i)
          else:
            i += 1
            
      listaOrdenada = bubbleSortPrioridade(itens)
      
      return (listaOrdenada + listaAuxiliar)
    
def bubbleSortData(lista):
  for x in lista:
    atual = 0
    while atual < len(lista) - 1:
        if formatoComparacaoData(lista[atual][1][0]) > formatoComparacaoData(lista[atual + 1][1][0]):
          temp = lista[atual]
          lista[atual] = lista[atual+1]
          lista[atual+1] = temp
        atual = atual + 1
        
  return lista
  
def ordenarPorData(itens):
     listaAuxiliar = []
     cont = 0
     i = 0
     while  i < len(itens):
          if itens[i][1][0] == "":
              listaAuxiliar.append(itens[i])
              itens.pop(i)
          else:
              i += 1        
     listaOrdenada = bubbleSortData(itens)
     return (listaOrdenada + listaAuxiliar)
    
def bubbleSortHora(lista):
  for x in lista:
    atual = 0
    while atual < len(lista) - 1:
        if (lista[atual][1][1]) > (lista[atual + 1][1][1]):
          temp = lista[atual]
          lista[atual] = lista[atual+1]
          lista[atual+1] = temp
        atual = atual + 1
        
  return lista
  
def ordenarPorHora(itens):
     listaAuxiliar = []
     cont = 0
     i = 0
     while  i < len(itens):
        if itens[i][1][1] == "":
            listaAuxiliar.append(itens[i])
            itens.pop(i)
        else:
            i += 1
     listaOrdenada = bubbleSortHora(itens)
     
     return (listaOrdenada + listaAuxiliar)
    
def listarFormatado(descricao, extras):
  novaAtividade = ""
  if descricao  == '' :
    return False
  else:
    for indice,i in enumerate(extras):       
        if indice == 2:
          if  i != "":
            novaAtividade += i + " " + descricao + " "
          else:
            novaAtividade += descricao + " "   
        else:
          if i != "":
            if indice == 0:
              i = dataFormatada(i) 
            elif indice == 1:
              i = horaFormatada(i)
            novaAtividade += i + " "

  return novaAtividade

def listarSemFormatacao(descricao, extras):
  novaAtividade = ""
  if descricao  == '' :
    return False
  else:
    for indice,i in enumerate(extras):       
        if indice == 2:
          if  i != "":
            novaAtividade += i + " " + descricao + " "
          else:
            novaAtividade += descricao + " "   
        else:
          if i != "":
            novaAtividade += i + " " 

  return novaAtividade

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def dataFormatada(data):
  return data[:2] + '/' + data[2:4] + '/' + data[4:]

def horaFormatada(hora):
  return hora[:2] + 'h' + hora[2:] + 'm'

RED_BOLD   = "\033[1;31m"
YELLOW = "\033[0;33m"
CYAN  = "\033[0;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
#BLUE  = "\033[1;34m"

def printCores(texto, cor) : 
  return (cor + texto + RESET)
 
def listar(lista):
  listaPrioridade = ["(A)","(B)","(C)","(D)"]
  listaCores = [ RED_BOLD,CYAN,YELLOW,GREEN]
  listagem = ""
  i = 0
  while i < len(lista):
    numeracao = lista[i][0]
    cond = False
    for indice,j in enumerate(listaPrioridade):
      if lista[i][1][1][2] == j or lista[i][1][1][2] == j.lower():
         listagem += str(numeracao) + " " + printCores(listarFormatado(lista[i][1][0],lista[i][1][1]),listaCores[indice])+ '\n'
         cond = True
    if cond == False:
          listagem += str(numeracao) + " " + listarFormatado(lista[i][1][0],lista[i][1][1])+ '\n'
    i += 1  
    
  return  listagem
    
def listaNumeracao(lista):
  listaAuxiliar = []
  fp = open(TODO_FILE, 'r')
  texto = fp.readlines()
  for indice,i in enumerate(lista):
    cond = True
    termoComparacao = listarSemFormatacao(i[0],i[1]).strip()
    contador = 0
    while contador < len(texto) and cond == True:
        if termoComparacao == texto[contador].strip():
          listaAuxiliar.append([contador + 1] + [i])
          cond = False
        else:
          contador += 1
  fp.close()
  return listaAuxiliar

def remover(lista,lista1,numero):
  cond = False
  for i in lista:
    for i in lista1:
      if i[0] == numero:
        compromisso = i[1]
        cond = True
  if cond == False:
    return False
  else:
    for indice,i in enumerate(lista):
        if i == compromisso:
          compromissoRemovido = lista.pop(indice)
    fp = open(TODO_FILE, 'w')
    for i in lista:
      fp.write(listarSemFormatacao(i[0],i[1]) + '\n')
    fp.close()

  return compromissoRemovido
  
# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'.

def listarPrioridade(descricao,extras,prioridade):
    novaAtividade = ""
    for indice,i in enumerate(extras):
        if indice == 2:
            if prioridade == '()':
              novaAtividade +=  descricao + " "
            else:
              novaAtividade +=  prioridade + " " + descricao + " "
        else:
          if i != "":
            novaAtividade += i + " " 

    return novaAtividade

def priorizar(lista,prioridade,numero):
    if prioridadeValida(prioridade) == False and prioridade != '()':
      print()
      print("ERRO!! Prioridade não válida,tente novamente.")
      return False
    cond = False
    listaArquivo = organizarArquivo()
    for i in lista:
      if i[0] == numero:
        compromisso = i[1]
        cond = True
    if cond == False:
      print("ERRO!! Número não existente no arquivo,tente novamente.")
      return False
    else:
      fp = open(TODO_FILE, 'w')
      for indice,i in enumerate(listaArquivo):
        if compromisso == i:
          fp.write(listarPrioridade(i[0],i[1],prioridade) + '\n')
        else:
          fp.write(listarSemFormatacao(i[0],i[1]) + '\n')
      fp.close()  

def fazer(numero):
  cond = False
  lista = listaNumeracao(listaOrdenada)
  for i in lista:
    if i[0] ==numero:
      cond = True
  if cond == False:
    return False
  else:
    compromissoFeito = remover(organizarArquivo(),listaNumeracao(listaOrdenada),numero)
    fp = open(ARCHIVE_FILE, 'a')
    fp.write(listarSemFormatacao(compromissoFeito[0],compromissoFeito[1]) + '\n')
    fp.close()

def menuOpcionalListar():
  listaParametros = ['Data','Hora','Prioridade','Contexto','Projeto','Sem Prioridades']
  cond = True
  while cond:
    filtragem = input("Deseja listar por: Data ou Hora ou Prioridade ou Contexto ou Projeto? [s/n] ").lower()
    while filtragem != 's' and filtragem != 'n':
      print()
      print("'Erro,digite apenas 's' para confirmar ou 'n' para não listar por filtragem")
      print()
      filtragem = input("Deseja listar por :Prioridade ou Data ou Hora ou Contexto ou Projeto? [s/n] ")
    if filtragem == 'n':
        cond = False
    else:
      #listaParametros = ['Data','Hora','Prioridade','Contexto','Projeto']
      print()
      print("(1) -> Data")
      print("(2) -> Hora")
      print("(3) -> Prioridade")
      print("(4) -> Contexto")
      print("(5) -> Projeto")
      print("(6) -> Sem Prioridades")
      print()
      opcao = int(input("Digite a opção de filtragem pelo critério desejado: "))
      while (opcao < 1) or (opcao > 6):
        print("Erro de numeração,digite um número válido!")
        print()
        print("(1) -> Data")
        print("(2) -> Hora")
        print("(3) -> Prioridade")
        print("(4) -> Contexto")
        print("(5) -> Projeto")
        print("(6) -> Sem Prioridades")
        print()
        opcao = int(input("Digite a opção de filtragem pelo critério desejado: "))
      print()
      print("="*50) 
      print(f"Você escolheu pela filtragem por ('{listaParametros[opcao -1]}')!")
      print("="*50)
      print()
      listaComparativa = listaNumeracao(listaOrdenada)
      lista = []
      listaVerificacoes = [dataValida,horaValida,prioridadeValida,contextoValido,projetoValido]
      if opcao != 6:
        parametroFiltro = input(f"Digite o parâmetro de filtro {listaParametros[opcao -1]}: ")
        if  opcao == 3:
          parametroFiltro = '(' + parametroFiltro + ')'
        while listaVerificacoes[opcao - 1](parametroFiltro) != True:
          print()
          print("Parâmetro inválido,digite novamente!")
          print()
          parametroFiltro = input(f"Digite o parâmetro de filtro {listaParametros[opcao -1]}: ")
          if  opcao == 3:
            print()
            parametroFiltro = '(' + parametroFiltro + ')'
        i = 0
        while i < len(listaComparativa):
            if parametroFiltro.lower() == listaComparativa[i][1][1][opcao - 1].lower():
                lista.append(listaComparativa[i])
            i += 1
        if lista == []:
          print()
          print(f"Não foi encontrado nenhum compromisso com o parâmetro {parametroFiltro}!")
          print()
        else:
          if dataValida(parametroFiltro) == True:
              print()
              print(f" == Todos os compromissos com a prioridade ({dataFormatada(parametroFiltro)}) : ==")
              print()
              print(listar(lista))
          elif horaValida(parametroFiltro) == True:
              print()
              print(f" == Todos os compromissos com a prioridade ({horaFormatada(parametroFiltro)}) : ==")
              print()
              print(listar(lista))
          else:
              print()
              print(f" == Todos os compromissos com a prioridade ({parametroFiltro}) : ==")
              print()
              print(listar(lista))
      else:
          i = 0
          while i < len(listaComparativa):
            if prioridadeValida(listaComparativa[i][1][1][2]) == False:
              lista.append(listaComparativa[i])
            i += 1
          print()
          print(" == Todos os compromissos sem prioridades: ==")
          print()
          print(listar(lista))
        
  #return 'saída'   

#Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.

def organizarArquivo():
      fp = open(TODO_FILE, 'r')
      lista = []
      texto = fp.readlines()
      for i in texto:
        texto = i.strip().split()
        #print(texto)
        lista += organizar(texto)
      fp.close()
      
      return lista
    
#UMA DAS ENTRADAS DA FUNCAO 'PROCESSARCOMANDOS'
    
ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
      comandos.pop(0) # remove 'agenda.py'
      comandos.pop(0) # remove 'adicionar'
      if len(comandos) == 0:
        print()
        print("ERRO!!! Compromisso para função adicionar vazio,tente novamente com pelo menos uma descrição!.")
        print()
      else: 
        itemParaAdicionar = organizar(comandos)[0]
        #itemParaAdicionar = organizar([' '.join(comandos)])[0]
        print()
        if adicionar(itemParaAdicionar[0],itemParaAdicionar[1]) == False:
          print()
          print("== Compromisso não adicionado,tente novamente. == ")
        else:    
          print()
          print("== Compromisso adicionado com sucesso!==")
     
  elif comandos[1] == LISTAR:
      comandos.pop(0)  # remove 'agenda.py'
      comandos.pop(0)  # remove 'listar'
      #print(listaOrdenada)
      #print(listaNumeracao(listaOrdenada))

      print(listar(listaNumeracao(listaOrdenada)))
      print()
      print()
      menuOpcionalListar()

  elif comandos[1] == REMOVER: 
      comandos.pop(0)  # remove 'agenda.py'
      comandos.pop(0)  # remove 'remover'
      try:
        numero = int(comandos.pop(0))
        print()
        if remover(organizarArquivo(),listaNumeracao(listaOrdenada),numero) == False:
          print(" == Erro!! Número não existente na listagem,tente novamente. ==")
        else:
          print("== Remoção de Compromisso feito com sucesso! ==")
          print()
      except:
          print()
          print("Erro!! Comando inválido.")

  elif comandos[1] == FAZER: 
      comandos.pop(0)  # remove 'agenda.py'
      comandos.pop(0)  # remove 'fazer'
      numero = int(comandos.pop(0))
      if fazer(numero) == False:
        print("== Erro!! Número não existente na listagem,tente novamente. == ")
      else:
        print()
        print("== Tarefa feita removida da agenda com sucesso! ==")
        print()

  elif comandos[1] == PRIORIZAR:
      comandos.pop(0)  # remove 'agenda.py'
      comandos.pop(0)  # remove 'priorizar'
      try:
        numero = int(comandos.pop(0))
        if type(numero) == int:
          prioridade = '(' + comandos.pop(0) + ')'
          if priorizar(listaNumeracao(listaOrdenada),prioridade,numero) == False:
            print()
            print("== Prioridade não alterada no sistema! == ")
          else:
            print()
            print("== Prioridade alterada com sucesso! ==")
      except:
        print()
        print("Erro!! Comando inválido.")
        
  else :
      print()
      print("Comando inválido.")

listaOrdenada = ordenarPorPrioridade(ordenarPorData(ordenarPorHora(organizarArquivo())))
      
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome'] """

processarComandos(sys.argv)


