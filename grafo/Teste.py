from strucs.Grafo import Grafo as Grafo
import numpy as np
import pandas as pd


grafo = Grafo()
grafo.createDataFrame("R0")
print(grafo.calcAdjacencia("R0"))

grafo = Grafo()
grafo.createDataFrame("R1")
print(grafo.calcAdjacencia("R0"))
#### invez de return set() coloca um texto bonito tipo Não há

grafo = Grafo()
grafo.digrafo = True
grafo.createDataFrame("R0")
print(grafo.calcAdjacencia("R0"))