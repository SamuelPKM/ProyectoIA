Muestra='abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789:!¡_-:;.,¿?=+*/  '
objetivo ='Creo que ya quedo este proyecto, cualquier cosa pueden modificarla o preguntarme, me desconecto por ahora y quedo al pendiente.' 
import datetime
import random
random.seed(3)
startTime = datetime.datetime.now()                                                                 
  #generacion aleatoria de genes
def Padres(length):
      genes = [] 
      while len(genes) < length: 
          Tamaño = min(length - len(genes), len(Muestra))
          genes.extend(random.sample(Muestra,Tamaño)) 
      return ''.join(genes) 
def Estado(x):
      return sum(1 for expected, actual in zip(objetivo,x) if expected == actual)
  #Mutacion 
def mutar(padre):
      index = random.randrange(0,len(padre))
      hijo = list(padre)
      nuevagen, alternate = random.sample(Muestra,2)
      hijo[index] = alternate if nuevagen == hijo[index] else nuevagen
      return ''.join(hijo)
def display(b):
      timeDiff = datetime.datetime.now() - startTime
      estado = Estado(b)
      print('{}\t{}\t{}'.format(b,estado,timeDiff))
#inicializar
mejorpadre = Padres(len(objetivo))
mejorestado = Estado(mejorpadre)
display(mejorpadre)
  #Creamos un ciclo para iterar 
while True:
      hijo = mutar(mejorpadre)
      nuevoEstado = Estado(hijo)
      if mejorestado >= nuevoEstado:
          continue
      display(hijo)
      if nuevoEstado >= len(mejorpadre):
          break
      mejorestado = nuevoEstado
      mejorpadre = hijo