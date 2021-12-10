#Muestras y Objetivo al cual nos acercaremos
Muestra='abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789:!¡_-:;.,¿?=+*/  '
objetivo ='El veloz murcielago hindu comia feliz cardillo y kiwi. La cigueña tocaba el saxofon detras del palenque de paja.'
#objetivo ='Hola mundo y todos quienes lo habitan, este soy yo, el proyecto final' 

import datetime
import random
random.seed(datetime.datetime.now())
startTime = datetime.datetime.now()                                                                 

#Generacion de los padres
def Padres(length):
      #Creamos una estructura vacia
      genes = [] 
      while len(genes) < length: 
          Tamaño = min(length - len(genes), len(Muestra))
          genes.extend(random.sample(Muestra,Tamaño)) 
      return ''.join(genes)

#Funcion de adecuacion
def Estado(x):
      return sum(1 for expected, actual in zip(objetivo,x) if expected == actual)

#Mutacion genetica de los individuos
def mutar(padre):
      index = random.randrange(0,len(padre))
      hijo = list(padre)
      nuevagen, alternate = random.sample(Muestra,2)
      hijo[index] = alternate if nuevagen == hijo[index] else nuevagen
      return ''.join(hijo)

#Mandamos a pantalla los resultados del mejor individuo
def display(b):
      timeDiff = datetime.datetime.now() - startTime
      estado = Estado(b)
      print('{}\t{}\t{}'.format(b,estado,timeDiff))

def Cruzar(padre):
      index = random.randrange(0,len(padre))
      hijo = list(padre)
      nuevagen, alternate = random.sample(Muestra,2)
      hijo[index] = alternate if nuevagen == hijo[index] else nuevagen


#Inicializar
mejorpadre = Padres(len(objetivo))
mejorestado = Estado(mejorpadre)
display(mejorpadre)

#Creamos un ciclo para iterar la seleccion, cruza y muta 
while True:
      x = random.randrange(1,100)
      hijo = mutar(mejorpadre)
      nuevoEstado = Estado(hijo)
      if mejorestado >= nuevoEstado:
          continue
      display(hijo)
      if nuevoEstado >= len(mejorpadre):
          break
      mejorestado = nuevoEstado
      mejorpadre = hijo