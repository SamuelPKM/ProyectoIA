import random
import statistics
import sys
import time
from enum import Enum
from math import exp


def _generar_padre(longitud, geneSet, obtener_aptitud):
    genes = []
    while len(genes) < longitud:
        tamañoMuestral = min(longitud - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, tamañoMuestral))
    aptitud = obtener_aptitud(genes)
    return Cromosoma(genes, aptitud, Estrategias.Creación)


def _mutar(padre, geneSet, obtener_aptitud):
    genesDelNiño = padre.Genes[:]
    índice = random.randrange(0, len(padre.Genes))
    nuevoGen, alterno = random.sample(geneSet, 2)
    genesDelNiño[índice] = alterno if nuevoGen == genesDelNiño[
        índice] else nuevoGen
    aptitud = obtener_aptitud(genesDelNiño)
    return Cromosoma(genesDelNiño, aptitud, Estrategias.Mutación)


def _mutar_personalizada(padre, mutación_personalizada, obtener_aptitud):
    genesDelNiño = padre.Genes[:]
    mutación_personalizada(genesDelNiño)
    aptitud = obtener_aptitud(genesDelNiño)
    return Cromosoma(genesDelNiño, aptitud, Estrategias.Mutación)


def _intercambiar(genesDePadre, índice, padres, obtener_aptitud, intercambiar,
                  mutar, generar_padre):
    índiceDeDonante = random.randrange(0, len(padres))
    if índiceDeDonante == índice:
        índiceDeDonante = (índiceDeDonante + 1) % len(padres)
    genesDelNiño = intercambiar(genesDePadre, padres[índiceDeDonante].Genes)
    if genesDelNiño is None:
        # padre y donante son indistinguibles
        padres[índiceDeDonante] = generar_padre()
        return mutar(padres[índice])
    aptitud = obtener_aptitud(genesDelNiño)
    return Cromosoma(genesDelNiño, aptitud, Estrategias.Intercambio)


def obtener_mejor(obtener_aptitud, longitudObjetivo, aptitudÓptima, geneSet, mostrar, mutación_personalizada=None, creación_personalizada=None, edadMáxima=None, tamañoDePiscina=1, intercambiar=None, segundosMáximos=None):
    if mutación_personalizada is None:
        def fnMutar(padre):
            return _mutar(padre, geneSet, obtener_aptitud)
    else:
        def fnMutar(padre):
            return _mutar_personalizada(padre, mutación_personalizada,
                                        obtener_aptitud)

    if creación_personalizada is None:
        def fnGenerarPadre():
            return _generar_padre(longitudObjetivo, geneSet, obtener_aptitud)
    else:
        def fnGenerarPadre():
            genes = creación_personalizada()
            return Cromosoma(genes, obtener_aptitud(genes),
                             Estrategias.Creación)

    búsquedaDeEstrategia = {
        Estrategias.Creación: lambda p, i, o: fnGenerarPadre(),
        Estrategias.Mutación: lambda p, i, o: fnMutar(p),
        Estrategias.Intercambio: lambda p, i, o:
        _intercambiar(p.Genes, i, o, obtener_aptitud, intercambiar, fnMutar,
                      fnGenerarPadre)
    }

    estrategiasUsadas = [búsquedaDeEstrategia[Estrategias.Mutación]]
    if intercambiar is not None:
        estrategiasUsadas.append(búsquedaDeEstrategia[Estrategias.Intercambio])

        def fnNuevoNiño(padre, índice, padres):
            return random.choice(estrategiasUsadas)(padre, índice, padres)
    else:
        def fnNuevoNiño(padre, índice, padres):
            return fnMutar(padre)

    for caducado, mejora in _obtener_mejoras(fnNuevoNiño, fnGenerarPadre,
                                             edadMáxima, tamañoDePiscina,
                                             segundosMáximos):
        if caducado:
            return mejora
        mostrar(mejora)
        f = búsquedaDeEstrategia[mejora.Estrategia]
        estrategiasUsadas.append(f)
        if not aptitudÓptima > mejora.Aptitud:
            return mejora


def _obtener_mejoras(nuevo_niño, generar_padre, edadMáxima, tamañoDePiscina,segundosMáximos):
    horaInicio = time.time()
    mejorPadre = generar_padre()
    yield segundosMáximos is not None and time.time() \
          - horaInicio > segundosMáximos, mejorPadre
    padres = [mejorPadre]
    aptitudesHistóricas = [mejorPadre.Aptitud]
    for _ in range(tamañoDePiscina - 1):
        padre = generar_padre()
        if segundosMáximos is not None and time.time() - horaInicio > \
                segundosMáximos:
            yield True, padre
        if padre.Aptitud > mejorPadre.Aptitud:
            yield False, padre
            mejorPadre = padre
            aptitudesHistóricas.append(padre.Aptitud)
        padres.append(padre)
    índiceDelÚltimoPadre = tamañoDePiscina - 1
    pÍndice = 1
    while True:
        if segundosMáximos is not None and time.time() - horaInicio > \
                segundosMáximos:
            yield True, mejorPadre
        pÍndice = pÍndice - 1 if pÍndice > 0 else índiceDelÚltimoPadre
        padre = padres[pÍndice]
        niño = nuevo_niño(padre, pÍndice, padres)
        if padre.Aptitud > niño.Aptitud:
            if edadMáxima is None:
                continue
            padre.Edad += 1
            if edadMáxima > padre.Edad:
                continue
            índice = bisect_left(aptitudesHistóricas, niño.Aptitud, 0,
                                 len(aptitudesHistóricas))
            proporciónSimilar = índice / len(aptitudesHistóricas)
            if random.random() < exp(-proporciónSimilar):
                padres[pÍndice] = niño
                continue
            mejorPadre.Edad = 0
            padres[pÍndice] = mejorPadre
            continue
        if not niño.Aptitud > padre.Aptitud:
            # mismo aptitud
            niño.Edad = padre.Edad + 1
            padres[pÍndice] = niño
            continue
        niño.Edad = 0
        padres[pÍndice] = niño
        if niño.Aptitud > mejorPadre.Aptitud:
            mejorPadre = niño
            yield False, mejorPadre
            aptitudesHistóricas.append(mejorPadre.Aptitud)


def ascenso_de_la_colina(funciónDeOptimización, es_mejora, es_óptimo, obtener_valor_de_característica_siguiente, mostrar, valorInicialDeCaracterística):
    mejor = funciónDeOptimización(valorInicialDeCaracterística)
    stdout = sys.stdout
    sys.stdout = None
    while not es_óptimo(mejor):
        valorDeCaracterística = obtener_valor_de_característica_siguiente(
            mejor)
        niño = funciónDeOptimización(valorDeCaracterística)
        if es_mejora(mejor, niño):
            mejor = niño
            sys.stdout = stdout
            mostrar(mejor, valorDeCaracterística)
            sys.stdout = None
    sys.stdout = stdout
    return mejor


class Cromosoma:
    def __init__(self, genes, aptitud, estrategia):
        self.Genes = genes
        self.Aptitud = aptitud
        self.Estrategia = estrategia
        self.Edad = 0


class Estrategias(Enum):
    Creación = 0,
    Mutación = 1,
    Intercambio = 2


class Comparar:
    def ejecutar(función):
        cronometrajes = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            horaInicio = time.time()
            función()
            segundos = time.time() - horaInicio
            sys.stdout = stdout
            cronometrajes.append(segundos)
            promedio = statistics.mean(cronometrajes)
            if i < 10 or i % 10 == 9:
                print("{} {:3.2f} {:3.2f}".format(
                    1 + i, promedio,
                    statistics.stdev(cronometrajes, promedio) if i > 1 else 0))