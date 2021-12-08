Muestra='abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789:!¡_-:;.,¿?=+*/  '
objetivo ='Foster The People - Pumped Up Kicks Official Video'
  
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

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
      estado = get_estado(b)
      print('{}\t{}\t{}'.format(b,estado,timeDiff))
#inicializar
mejorpadre = generate_padre(len(objetivo))
mejorestado = get_x(mejorpadre)
display(mejorpadre)
  
  #Creamos un ciclo para iterar 
while True:
      child = mutar(mejorpadre)
      childFitness = get_estado(hijo)
      if mejorestado >= x:
          continue
      display(child)
      if Estado >= len(mejorpadre):
          break
      mejorestado = x
      mejorpadre = x