# from django.test import TestCase

# # Create your tests here.
# from cgi import print_form
# from structs.Grafo import Grafo as Grafo
# import numpy as np
# import pandas as pd


# grafo = Grafo()
# grafo.createDataFrame("R0 R1 5\nR1 R2 7\nR2 R1 9 4 \nR2 R3 3")
# grafo = grafo.dataframe.iloc[:,:2].values.tolist()

# class Digrafo:
#     """ Digrafo utilizando lista de adjacencia. """

#     def __init__(self, arestas): 
#         self.lista_adjacente = {}
#         for i in arestas:
#             if i[0] not in self.lista_adjacente.keys():
#                 self.lista_adjacente[i[0]] = []

#             if i[1] not in self.lista_adjacente.keys():
#                 self.lista_adjacente[i[1]] = []
#         self.vertices = list(self.lista_adjacente.keys())
    
#     def inserir(self, u, w):
#         self.lista_adjacente[u].append(w)

#     def mostrar(self):
#         print(self.lista_adjacente)
#         for i in self.lista_adjacente.keys():
#             print(f"{i}: {', '.join(str(x) for x in self.lista_adjacente[i])}")

#     def kosaraju(self, digrafo_transposto):
#         """ 
#         Algoritmo de Kosaraju (1978) obtém os componentes fortemente conexos do grafo orientado. 
#         1. Execute DFS(G) para obter f[v] para v ∈ V
#         2. Obter o grafo transposto GT (é passado por parametro)
#         3. Execute DFS(GT) considerando os vértices em ordem decrescente de f[v].
#         4. Devolva os conjuntos de vértices de cada árvore da floresta de busca em profundidade obtida
#         """

#         visitados = {}
#         for i in self.lista_adjacente.keys():
#             visitados[i] = False
        
#         ordem = []  # Vetor dos tempos de finalização de cada vértice

#         for vertice in self.lista_adjacente.keys():
#             if not visitados[vertice]:
#                 self.DFS(vertice, ordem, visitados)
        
#         return self.DFS_transponto(digrafo_transposto, ordem)

    
#     def DFS(self, u, ordem, visitados):
#         """ Faz a busca em profundidade para obter os tempos de finalização. """
        
#         visitados[u] = True

#         for w in self.lista_adjacente[u]:
#             if not visitados[w]:
#                 self.DFS(w, ordem, visitados)
        
#         ordem.append(u)


#     def DFS_transponto(self, digrafo_transposto, ordem):
#         """ 
#         Executa a busca em profundidade (iterativa) considerando os vertices em ordem decrescente no vetor de tempos
#         de finalização e retorna os conjuntos de vértices obtidos que são os componentes fortemente conexos do digrafo.
#         """
        
#         visitados = {}
#         for i in self.lista_adjacente.keys():
#             visitados[i] = False
#         componentes = []

#         for vertice in range(len(ordem) - 1, -1, -1):
#             if not visitados[ordem[vertice]]:
#                 pilha = [ordem[vertice]]
#                 visitados[ordem[vertice]] = True
#                 componente = set()  # SCC (Componente fortemente conexo)

#                 while len(pilha) > 0:
#                     u = pilha.pop() 

#                     for w in digrafo_transposto.lista_adjacente[u]:
#                         if not visitados[w]:
#                             visitados[w] = True
#                             pilha.append(w)
                    
#                     componente.add(u)

#                 componentes.append(componente)
        
#         return componentes


# if __name__ == "__main__":
#     #arestas = [['R0', 'R1'], ['R1', 'R2'], ['R2', 'R1'], ['R2', 'R3']]
#     arestas = [['A', 'B'], ['A', 'D'], ['B', 'C'], ['C', 'B'], ['C', 'E'], ['D', 'A'], ['D', 'C'], ['D', 'E']] # grafo do slide conceitos_basicos pag.28

#     digrafo = Digrafo(arestas)
#     #digrafo = Digrafo(grafo) #para usar o grafo lá de cima
#     digrafo_transposto = Digrafo(arestas)
#     #digrafo_transposto = Digrafo(arestas) #para usar o grafo lá de cima
    

#     for aresta in arestas:
#         digrafo.inserir(aresta[0], aresta[1])
#         digrafo_transposto.inserir(aresta[1], aresta[0])

#     print(f"\nComponentes fortemente conexos: {digrafo.kosaraju(digrafo_transposto)}\n")