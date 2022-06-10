from strucs.Grafo import Grafo as Grafo
import numpy as np
import pandas as pd


grafo = Grafo()
grafo.createDataFrame("R0 R1 155 0\nR3 R1 155 0")
print(grafo.dataframe)
grafo.createImg()

