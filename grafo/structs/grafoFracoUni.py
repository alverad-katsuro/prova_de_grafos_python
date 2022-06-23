import numpy as np
import pandas as pd

from . import Grafo as Grafo

def conversaoDataMatriz(grafoOriginal):
    grafoData =  grafoOriginal.dataframe.iloc[:,:2].values.tolist()
    #print(grafoData)

    #print(grafo.dataframe)
    #grafo.createImg()
    vert = set()
    for i in grafoData:
        for j in i:
            if j not in vert:
                vert.update({j}) #adiciona o vertices no conjunto pra saber quem e

    l = list(vert) #converte para lista total de vertices
    l.sort()
    #print(l)
    count = len(l)

    #faz matriz de adjacencia
    graph = [0] * count
    for i in graph:
        graph[graph.index(i)] = [0] * count #cria a lista da lista (colunas da matriz)

    #def printg(graph):
    #    for i in graph:
    #        print(i)

    for i in l: #linha matriz adj
        g = l.index(i) #localiza vertice na lista
        for k in l: #coluna matriz adj
            if i != k:
                for v in grafoData: # loop pra procurar vertice i na matriz original
                    if v[0] == i:
                        if k == v[1]: #checar se vertice conectado a vertice i e o vertice k, caso positivo bota 1
                            graph[g][l.index(k)] = 1

    #printg(graph)
    # multiplicando matriz adj por ela mesma V vezes pra ter matriz caminho
    b = np.array(graph)
    c = np.array(graph)
    for i in range(count):
        b = b + np.dot(b,c)

    #print("matriz caminho antes\n", b, "\n")
    lin = 0
    for i in b:
        col = 0
        for j in i:
            if j > 1: # substitui numeros maiores que 1 por 1 na matriz caminho
                b[lin][col] = 1
            col +=1
        lin += 1
    #print("matriz caminho depois\n", b, "\n")
    # retorna matriz caminho e contagem de vertices
    return b, count

def checarConexidade(graph, n):
    strongly = True # checa se grafo é fortemente conexo
    for i in range(n):
        for j in range(n):
            # se todos os elementos nao forem iguais entao o grafo nao e fortemente conectado
            if (graph[i][j] != graph[j][i]):
                strongly = False
                break
        if not strongly:
           break
    if (strongly):
        return "Fortemente conexo"  

    # checa se grafo e unilateral pela matriz triangular superior
    uppertri = True
    for i in range(n):
        for j in range(n):
            # Se  algum elemento do triangulo superior for 0, entao falso
            if (i > j and graph[i][j] == 0):
                uppertri = False
                break;            
        if not uppertri:
            break;    
    if uppertri:
        return "Unilateralmente Conexo"

    # checa se grafo e unilateral pela matriz triangular inferior
    lowertri = True
    for i in range(n):
        for j in range(n):
            # Se  algum elemento do triangulo inferior for 0, entao falso
            if (i < j and graph[i][j] == 0):
                lowertri = False
                break
        if not lowertri:
            break;        
    if lowertri:
        return "Unilateralmente Conexo"
    # Se elementos estao em ordem aleatoria e nao sincronizados entao e fraco
    else:
        return "Fracamente Conexo"

#if __name__ == "__main__":
#    grafo = Grafo()
#    grafo.createDataFrame("R0 R1 155 0\nR1 R2 155 1\nR2 R3 155 1 \nR3 R1 155 1")
    
#    graph, n = conversaoDataMatriz(grafo)

#    resultado = checarConexidade(graph, n)
#    print(resultado)
