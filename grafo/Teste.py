from structs.Grafo import Grafo as Grafo
import numpy as np
import pandas as pd


grafo = Grafo()
#grafo.createDataFrame("A B 7\nB C 8\nA D 5\nD F 6\nE G 9\n E F 8\n D E 15\n E B 7")
#grafo.createDataFrame("A B\n B C\n C D\nD A\n D E")

grafo.createDataFrame("A B 7\nB C 8\nA D 5\nB D 9\nD F 6\nF G 11\nE G 9\n E F 8\n D E 15\n B E 7\nC E 5\n")
#grafo.createDataFrame("A B 7\nB C 8\nA D 5\nD E 8\n B D 0\n")
#grafo.createDataFrame("R0 R1 155 0\nR1 R2 155 1\nR2 R3 155 1 \nR3 R1 155 1")
grafo.digrafo = True
grafo.createImg()
print(grafo.conexidadeGrafo(force=True))
#print(grafo.dataframe)
#grafo.createDataFrame("A")
#grafo.digrafo = False
#grafo.createImg()

#print(grafo.dataframe)
#grafo.createImg()
#print(grafo.buscaProfundidade002(identify_cycle=True))
#print(grafo.calcAdjacencia("A"))
#print(grafo.hasCiclo())
#grafo.AGM()
#print(grafo.dataframe)
#grafo.createImg()

#print(grafo.conexidadeNotDigrafo())
