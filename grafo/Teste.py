from strutcs.Grafo import Grafo as Grafo
import numpy as np
import pandas as pd


grafo = Grafo()
grafo.createDataFrame("R0 R1\nR1 R2\nR2 R1")

print(grafo.containsAresta("R3", "R0"))
#print(grafo.conexidadeNotDigrafo())
