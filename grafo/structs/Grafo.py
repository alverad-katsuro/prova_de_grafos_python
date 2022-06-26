from typing import Type
import numpy as np
import pandas as pd

from base64 import b64encode
from graphviz import Digraph, Graph

import sys
import copy

class Grafo():
    def __init__(self, digrafo = False):
        """Inicializa um grafo mediante instanciação de um Dataframe, 
          em que se possuem as seguintes colunas:
          origem, que é de onde a orientação sai, caso possua;
          destino, que é de onde a orientação vai, caso possua;
          label, que é o valor da aresta que sai de um vértice e vai para outro vértica;
          cluster, que é um subconjunto de vértices que podem ser formados em um único grafo;
          
        Args:
          digrafo (bool): Valor booleano que define a orientação do grafo. 
          Orientado, caso Verdadeiro; Não-orientado, caso Falso.
        """
        self.dataframe = pd.DataFrame(columns=["origem", "destino", "label", "cluster"])
        self.digrafo = digrafo
        self.log = []
        self.imagem_bin = {}
        self.lista_adjacente = {}
        self.lista_adjacente_transposta = {}
        self.vertices = []
        self.matrizCaminho = []

    def inserir_adjcencia(self, u, w):
            self.lista_adjacente[u].append(w)

    def inserir_adjcencia_transposta(self, u, w):
            self.lista_adjacente_transposta[u].append(w)

    def mostrar(self):
        print(self.lista_adjacente)
        for i in self.lista_adjacente.keys():
            print(f"{i}: {', '.join(str(x) for x in self.lista_adjacente[i])}")


    def __startAdj(self):
        for i in self.dataframe.iloc[:,:2].values.tolist():
            if i[0] not in self.lista_adjacente.keys():
                self.lista_adjacente[i[0]] = []

            if i[1] not in self.lista_adjacente.keys():
                self.lista_adjacente[i[1]] = []

    def __startAdjTrans(self):
        for i in self.dataframe.iloc[:,:2].values.tolist():
            if i[0] not in self.lista_adjacente_transposta.keys():
                self.lista_adjacente_transposta[i[0]] = []

            if i[1] not in self.lista_adjacente_transposta.keys():
                self.lista_adjacente_transposta[i[1]] = []

    def comp_forts(self):
        self.__startAdj()
        self.__startAdjTrans()
        for aresta in self.dataframe.iloc[:,:2].values.tolist():
            self.inserir_adjcencia(aresta[0], aresta[1])
            self.inserir_adjcencia_transposta(aresta[1], aresta[0])
        return self.__kosaraju()
        

    def __kosaraju(self):
        """ 
        Algoritmo de Kosaraju (1978) obtém os componentes fortemente conexos do grafo orientado. 
        1. Execute DFS(G) para obter f[v] para v ∈ V
        2. Obter o grafo transposto GT (é passado por parametro)
        3. Execute DFS(GT) considerando os vértices em ordem decrescente de f[v].
        4. Devolva os conjuntos de vértices de cada árvore da floresta de busca em profundidade obtida
        """

        visitados = {}
        for i in self.lista_adjacente.keys():
            visitados[i] = False
        
        ordem = []  # Vetor dos tempos de finalização de cada vértice

        for vertice in self.lista_adjacente.keys():
            if not visitados[vertice]:
                self.DFS(vertice, ordem, visitados)

        return self.DFS_transposto(ordem)

    
    def DFS(self, u, ordem, visitados):
        """ Faz a busca em profundidade para obter os tempos de finalização. """
        
        visitados[u] = True

        for w in self.lista_adjacente[u]:
            if not visitados[w]:
                self.DFS(w, ordem, visitados)
        
        ordem.append(u)


    def DFS_transposto(self, ordem):
        """ 
        Executa a busca em profundidade (iterativa) considerando os vertices em ordem decrescente no vetor de tempos
        de finalização e retorna os conjuntos de vértices obtidos que são os componentes fortemente conexos do digrafo.
        """
        
        visitados = {}
        for i in self.lista_adjacente.keys():
            visitados[i] = False
        componentes = []

        for vertice in range(len(ordem) - 1, -1, -1):
            if not visitados[ordem[vertice]]:
                pilha = [ordem[vertice]]
                visitados[ordem[vertice]] = True
                componente = set()  # SCC (Componente fortemente conexo)

                while len(pilha) > 0:
                    u = pilha.pop() 

                    for w in self.lista_adjacente_transposta[u]:
                        if not visitados[w]:
                            visitados[w] = True
                            pilha.append(w)
                    
                    componente.add(u)

                componentes.append(componente)
        
        return componentes

    def getVertices(self):
        """Retorna todos os vértices de um grafo, sem repetição e sem ordem específica
        
          Returns:
            Conjunto de vértices do Grafo, de ordem não fixa e sem repetição.
        """
        vertices = set()
        for _, row in self.dataframe.iterrows():
            if (not pd.isnull(row["destino"])):
                vertices.add(row["origem"]) 
                vertices.add(row["destino"]) 
            else:
                vertices.add(row["origem"]) 
        return vertices

    def containsAresta(self, *args):
        """Verifica a existência de uma aresta no grafo: caso possua em um grafo,
        em um vértice do grafo ou entre dois vértices em específico.
        
        Correspondente ao requisito 1.
          
        Args:
          *args: caso *args possua nenhum argumento, verifica a existência de uma aresta
          no grafo; caso possua um argumento, que deve ser o nome de um vértice,
          verifica a existência de uma aresta no vértice inserido; caso possua
          dois argumentos, que devem ser o nome de dois vértices, verifica a existência
          de uma aresta entre esses dois vértices.
            
        Returns:
          Verdadeiro, caso a aresta exista; Falso, caso não exista.
        """
        if len(args) == 0:
          return self.__hasAresta1()
        elif len(args) == 1 and isinstance(args[0], str):
          return self.__hasAresta2(args[0])
        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
          return self.__hasAresta3(args[0], args[1])

    def __hasAresta1(self): 
        #Requisito 1: Verificar a existencia de uma aresta.
        return False if (self.dataframe["destino"].isnull().values.all()) else True

    def __hasAresta2(self, inp1): 
        #Requisito 1: Verificar a existencia de uma aresta em determinado vertice.
        return True if (self.calcGrau(inp1) > 0) else False

    def __hasAresta3(self, inp1, inp2): 
        #Requisito 1: Verificar a existencia de uma aresta entre dois vertices.
        for _, row in self.dataframe.iterrows():
          if (((row["origem"] == inp1) and (row["destino"] == inp2)) or ((row["origem"] == inp2) and (row["destino"] == inp1))):
            return True
        return False

    def __createAresta(self, origem, destino=np.nan, label=np.nan, cluster=np.nan):
        """Cria as linhas do DataFrame.        
        Args:
            origem: vértice inicial, requisito mínimo para geração de um grafo; 
            destino: vértice final, criando uma aresta da origem até o destino caso
            passada como argumento;
            label: label da aresta, podendo conter o peso e o custo formatados;
            cluster: subgrafo organizado em grupo.
        """      
        if len(self.dataframe.query("(origem == @origem) & (destino == @destino) & (label == @label) & (cluster == @cluster)")) == 0:
            self.dataframe = pd.concat(
            [self.dataframe, 
            pd.DataFrame([[origem, destino, label, cluster]], 
            columns=["origem", "destino", "label", "cluster"])
            ], 
            ignore_index=True
            )

    def __countAresta3(self, inp1, inp2): 
        """Conta o número de arestas contidas entre dois vértices
                  
        Args:
          inp1, inp2: nome dos vértices que se deseja contar o número de arestas entre
            
        Returns:
          O número de arestas entre os vértices em questão.
        """
        n_arestas = 0
        for _, row in self.dataframe.iterrows():
          if (((row["origem"] == inp1) and (row["destino"] == inp2)) or ((row["origem"] == inp2) and (row["destino"] == inp1))):
            n_arestas +=1
        return n_arestas


    def __calcVizinhoGeneric(self, input_name): 
        """Calcula a adjacência de um vértice de um grafo não-orientado.
        
        Correspondente ao requisito 3.
          
        Args:
          input_name (String): nome do vértice que se deseja calcular a adjacência.
            
        Returns:
          A adjacência do vértice, que inclui a superior e a inferior.
        """
        viz = set()
        for _, row in self.dataframe.iterrows():
          if ((row["origem"] == input_name) and (not pd.isnull(row["destino"]))):
            viz.add(row["origem"])
            viz.add(row["destino"])
          elif ((row["origem"] == input_name) and (pd.isnull(row["destino"]))):
            viz.add(row["origem"])
          elif (row["destino"] == input_name):
            viz.add(row["origem"])
            viz.add(row["destino"])
          else:
            continue
        return viz

    def __calcVizinhoSucessor(self, input_name): 
        """Calcula a adjacência superior de um vértice de um grafo orientado.
        
        Correspondente ao requisito 3.
          
        Args:
          input_name (String): nome do vértice que se deseja calcular a adjacência.
            
        Returns:
          A adjacência superior do vértice;
        """
        viz = set()
        for _, row in self.dataframe.iterrows():
          if ((row["origem"] == input_name) and (not pd.isnull(row["destino"]))):
            viz.add(row["origem"])
            viz.add(row["destino"])
          elif ((row["origem"] == input_name) and (pd.isnull(row["destino"]))):
            viz.add(row["origem"])
          else:
            continue
        return viz

    def __calcVizinhoAntecessor(self, input_name): 
        """Calcula a adjacência inferior de um vértice de um grafo orientado.
        
        Correspondente ao requisito 3.
          
        Args:
          input_name (String): nome do vértice que se deseja calcular a adjacência.
            
        Returns:
          A adjacência inferior do vértice;
        """
        viz = set()
        for _, row in self.dataframe.iterrows():
          if (row["destino"] == input_name):
            viz.add(row["destino"])
            viz.add(row["origem"])
          else:
            if (row["origem"] == input_name):
              viz.add(row["origem"])
        return viz

    def calcGrau(self, input_name): 
        """Calcula o grau de um vértice de um grafo orientado ou não-orientado.
        
        Correspondente ao requisito 2.
          
        Args:
          input_name (String): nome do vértice que se deseja calcular o grau.
            
        Returns:
          O grau do vértice em questão.
        """
        grau = 0
        for _, row in self.dataframe.iterrows():
          if ((row["origem"] == input_name) or (row["destino"] == input_name)):
            if (row["origem"] == row["destino"]):
              grau += 2
            else: 
              grau += 1
          else:
            continue
        return grau

    def calcAdjacencia(self, input_name, sucessor=False): 
        """Calcula a adjacência de um vértice de um grafo orientado ou não-orientado.
        
        Correspondente ao requisito 3.
          
        Args:
          input_name (String): nome do vértice que se deseja calcular a adjacência.
          sucessor (bool): caso Verdadeiro, retorna apenas a adjacência superior do
          grafo orientado; caso Falso, retorna a adjacência superior e inferior do
          grafo orientado.
            
        Returns:
          caso orientado e com sucessor=True, a adjacência superior do vértice;
          caso orientado e com sucessor=False, uma tupla com a adjacência superior
          e inferior do vértice;
          caso não-orientado, a adjacência do vértice, que inclui a superior e a 
          inferior.
        """
        if self.digrafo:
          if sucessor:
            return self.__calcVizinhoSucessor(input_name)
          return self.__calcVizinhoSucessor(input_name).union(self.__calcVizinhoAntecessor(input_name))
        else:
          return self.__calcVizinhoGeneric(input_name)

    def conexidadeGrafo(self, force=False): 
        """Verifica se um grafo é conexo ou desconexo, e caso seja 
           um grafo orientado, pode verificar a força do grafo.
           
        Correspondente ao requisito 4, e à parte do requisito 5, 6, 7.
          
        Args:
          force (bool): caso Verdadeiro, se for passado um grafo orientado, 
          calcula a força do mesmo (fortemente conexo, unilateralmente conexo, 
          fracamente conexo, desconexo); caso Falso, para grafos orientados e
          não-orientados, retorna se o grafo é conexo ou desconexo.
            
        Returns:
          caso orientado e com force=True, retorna se o grafo é fortemente conexo,
          unilateralmente conexo ou fracamente conexo;
          caso orientado e com force=False, retorna se o grafo é conexo ou desconexo;
          caso não-orientado, retorna se o grafo é conexo ou desconexo.
        """
        if self.digrafo:
          self.digrafo = False
          conexidade = self.buscaProfundidade002(identify_conexidade=True)
          self.digrafo = True
                      
          if conexidade and force:
            return self.__checarConexidade()
          return conexidade 
        else:
          return self.buscaProfundidade002(identify_conexidade=True)

    def hasCiclo(self):
        """Verifica se um grafo possui algum ciclo.
            Requisito 8

        Returns:
          Verdadeiro, caso possua ciclo; Falso, caso não possua ciclo.
        """
        if self.digrafo:
          return self.buscaProfundidade001(identify_cycle=True)
        else:
          if self.isMultigrafo():
            return True
          return self.buscaProfundidade002(identify_cycle=True)
        
    def isMultigrafo(self):
        """Verifica se um grafo não-orientado é um multigrafo, ou seja,
        se possui algum self-loop ou se possui mais que uma ligação entre 
        dois vértices iguais.

        Returns:
          Verdadeiro, caso seja multigrafo; Falso, caso não seja um multigrafo.
        """
        if not self.digrafo:
          vertices = list(self.getVertices())
          for i in range(0, len(vertices)):
            for j in range(0, len(vertices)):
              if vertices[i] == vertices[j]:
                if self.__hasAresta3(vertices[i], vertices[j]):
                  return True
              if self.__countAresta3(vertices[i], vertices[j]) > 1:
                return True
          return False
    
    def buscaProfundidade001(self, identify_cycle=False):
        """Verifica se um grafo (orientado) possui algum ciclo através de 
        uma busca em profundidade. Por utilizar um conjunto, a ordem dos elementos 
        não é preservada, o que faz com que cada execução do código possa retornar 
        uma ordem diferente de outra execução, apesar que correta.
            
        Args:
          identify_cycle (bool): caso Verdadeiro, o algoritmo visa identificar a 
          existência de ciclo; caso Falso, o algoritmo visa encontrar a ordem de 
          saturação dos vértices.
        Returns:
          Ordem crescente em que os vértices são saturados, caso identify_cycle=False;
          Existência de ciclo, caso identify_cycle=True.
        """
        conjunto_vertices = self.getVertices()
        used = []
        adjacencia = set()
        order = []
        done = []
        element1 = 0
        if (self.digrafo):
          count = len(conjunto_vertices)
          while (count != len(done)):
            print('original', conjunto_vertices)
            print('queue', order)
            print('cortados/preto', done)

            if (len(order) == 0):
              element1 = conjunto_vertices.pop()
              print('new_choice: ', element1)
              if element1 not in used:
                used.append(element1)
              adjacencia = self.__calcVizinhoSucessor(element1) - set([element1])
            else: 
              element1 = order.pop()
              print('new_choice: ', element1)
              if element1 not in used:
                used.insert(len(used), element1)
              if element1 in conjunto_vertices:
                conjunto_vertices.remove(element1)
              adjacencia = self.__calcVizinhoSucessor(element1) - set([element1])
              for element in adjacencia:
                if element in done and element in order:
                  order.remove(element)
 
            print(element1)
            if identify_cycle:
              for element in adjacencia:
                if (element not in conjunto_vertices) and (element in order):
                  return True

            if (len(adjacencia) == 0):
              if element1 not in done:
                done.append(element1)
              print('corta folha', element1)
              continue
            else:
              if all(item in done for item in adjacencia):
                if element1 not in done:
                  done.append(element1)
                adjacencia = set()
                continue
              else:
                order.append(element1)
            print(f"{element1} -> {adjacencia}")

            for element in adjacencia:
            #  print("i am at", element)
              if ((element in conjunto_vertices) or (element not in order)):
                order.append(element)
              else:
                print(f'element {element} was already visited!')
            adjacencia = set()

          if (identify_cycle):
            return False
          print('used: ', used)
          print('done: ', done)

          done.reverse()

          return done

    def __conversaoDataMatriz(self):
        grafoData =  self.dataframe.iloc[:,:2].values.tolist()
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
        self.matrizCaminho = b


    def __checarConexidade(self):
        n = len(self.matrizCaminho)
        strongly = True # checa se grafo é fortemente conexo
        for i in range(n):
            for j in range(n):
                # se todos os elementos nao forem iguais entao o grafo nao e fortemente conectado
                if (self.matrizCaminho[i][j] != self.matrizCaminho[j][i]):
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
                if (i > j and self.matrizCaminho[i][j] == 0):
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
                if (i < j and self.matrizCaminho[i][j] == 0):
                    lowertri = False
                    break
            if not lowertri:
                break;        
        if lowertri:
            return "Unilateralmente Conexo"
        # Se elementos estao em ordem aleatoria e nao sincronizados entao e fraco
        else:
            return "Fracamente Conexo"

    def buscaProfundidade002(self, identify_cycle=False, identify_conexidade=False):
        """Verifica se a ordem de exclusão dos vértices de um grafo (não-orientado),
        ou verifica se possui algum ciclo ou a conexidade do grafo através de uma
        busca em profundidade. Por utilizar um conjunto, a ordem dos elementos 
        não é preservada, o que faz com que cada execução do código possa retornar 
        uma ordem diferente de outra execução, apesar que correta.
            
        Args:
          identify_cycle (bool): caso Verdadeiro, o algoritmo visa identificar a 
          existência de ciclo;
          identify_conexidade (bool): caso Verdadeiro, o algoritmo visa identificar a 
          existência de conexidade;
        Returns:
          Ordem crescente em que os vértices são saturados, caso identify_cycle=False 
          e identify_conexidade=False;
          Existência de ciclo, caso identify_cycle=True.
          Conexidade, caso identify_cycle=False e identify_conexidade=True.
        """
        conjunto_vertices = self.getVertices()
        used = []
        adj = []
        adjacencia = []
        order = []
        done = []
        if identify_conexidade:
          conexo = 0
        if not self.digrafo:
          count = len(conjunto_vertices)
          while (count != len(done)):
            print('original', conjunto_vertices)
            print('queue', order)
            print('cortados/preto', done)
            if identify_cycle:
              for e0_ele in order:
                if (order.count(e0_ele) > 1):
                  print("welp")
                  return True
            if (len(order) == 0):
              element1 = conjunto_vertices.pop()
              print('new_choice: ', element1)
              if element1 not in used:
                used.append(element1)
                adj = self.__calcVizinhoGeneric(element1) 
              if identify_conexidade:
                conexo += 1
            else: 
              element1 = order.pop()
              print('new_choice: ', element1)
              if element1 not in used:
                used.append(element1)
                adj = self.__calcVizinhoGeneric(element1) 
              if element1 in conjunto_vertices:
                conjunto_vertices.remove(element1)

            for e_ele in adj:
              adjacencia.append(e_ele)
              if element1 in adjacencia:
                adjacencia.remove(element1)
              for elementx in done:
                if elementx in adjacencia:
                  adjacencia.remove(elementx)

            print('adj', adjacencia)
      
            if ((len(adjacencia) == 0) or (all(item in used for item in adjacencia))):
              if element1 not in done:
                done.append(element1)
              print('corta folha', element1)
   
              adjacencia = []
              continue
            else:
              if (all(item in done for item in adjacencia)) or (all(item in used for item in adjacencia)):
                if element1 not in done:
                  done.append(element1)
                print('corta folha', element1)
                adjacencia = []
                continue
              else:
                order.append(element1)

            print(f"{element1} -> {adjacencia}")

            for element in adjacencia:
              if ((element in conjunto_vertices) or (element not in order)):
                order.append(element)
              else:
                print(f'element {element} was already visited!')
 
            adjacencia = []

          if identify_cycle:
            return False
          if identify_conexidade:
            print("conexo", conexo)
            return True if conexo == 1 else False
          print('used: ', used)
          print('done: ', done)
          done.reverse()
          return done

    def ordenacaoTopologica(self): 
        """Calcula a ordenação topológica de um grafo orientado, acíclico e conexo,
        e gera a imagem do mesmo.

        Correspondente ao requisito 9.
        """        
        if self.digrafo and not self.buscaProfundidade001(identify_cycle=True) and self.conexidadeGrafo():
          list_order = self.buscaProfundidade001()
          self.imagem_bin["topologica"] = self.createImg(ordering=list_order)

    def ordTopologica(self):
        list_order = []
        if self.digrafo and not self.buscaProfundidade001(identify_cycle=True): #not verifying conexidade
          list_order = self.buscaProfundidade001()

        return list_order

    def getWeightNNodeFromNode(self, i):
      """ Returns:
            Uma lista com os vertices vizinhos e os pesos de suas arestas (vizinho, peso)
            a partir da origem i
      """
      dest_node = ''
      weight_dest = 0
      nodeNodeNWeight = ('', 0)
      list_nodeNodeNWeight = []
      for _, row in self.dataframe.iterrows():
      
        if ((row["origem"] == i)):
          dest_node = row["destino"]
          
          
          weight_dest = row["label"]
          nodeNodeNWeight = (dest_node, int(weight_dest))
          list_nodeNodeNWeight.append(nodeNodeNWeight)
          
      print("dn",dest_node)
      print(weight_dest)
     
      return list_nodeNodeNWeight

    def getCurrNParentNWeight(self):
      """ Avalia todas as ligacoes(edges) do grafo

          Returns:
            Uma lista com tuplas contendo
            (o vertices atual, o vertice parente, o peso da aresta entre os dois)
      """
      dest_node = ''
      weight_dest = 0
      currNParentNWeight = ('','', 0)
      
      list_nodeNodeNWeight = []
      for _, row in self.dataframe.iterrows():
             
        curr_node = row["origem"]
        dest_node = row["destino"]      
        weight_dest = row["label"]

        nodeNodeNWeight = (curr_node, dest_node, int(weight_dest))
        list_nodeNodeNWeight.append(nodeNodeNWeight)
          
      return list_nodeNodeNWeight
  

    def defaultLabelToOne(self):

      """ Caso o grafo seja nao ponderado, ou seja, os labels são null eles são trocados para o peso padrao 1
          permitindo o calculo do menor caminho em grafos nao ponderados
          
          Returns:
            Retorna um novo grafo com os labels como 1

          !Requisito 11!
      """ 

      vertices = set()
      newGraph = self
      for _, row in self.dataframe.iterrows():
        if (not pd.isnull(row["destino"])):
          #vertices.add(row["origem"]) 
          #vertices.add(row["destino"])
          if (pd.isnull(row["label"])):
            row["label"] = 1
            newGraph = row["label"]
        
      return newGraph



    def bellmanFord(self, src, goal):
      """ Executa o algoritmo de bellmanFord a partir de uma origem(src) até um alvo(goal)
          

          Returns:
            Uma lista com as menores distancias da origem para todos dos vertices
            e uma lista de vertices na ordem do menor caminho da origem até o alvo

          !Requisito 11!
      """ 
    
      print(self.defaultLabelToOne())
      self = self.defaultLabelToOne()
      vertices = self.getVertices()
      V = len(self.getVertices())
      vertices = list(vertices)
      path = []

      previousNode = [0] * V
      list_dists = []
      dist = [float("Inf")] * V
      dist[vertices.index(src)] = 0
      
      for _ in range(V -1):
        for u, v, w in self.getCurrNParentNWeight():
          if dist[vertices.index(u)] != float("Inf") and dist[vertices.index(u)] + w < dist[vertices.index(v)]:

            dist[vertices.index(v)] = dist[vertices.index(u)] + w
            previousNode[vertices.index(v)] = (u)

      for u, v, w in self.getCurrNParentNWeight():
        if dist[vertices.index(u)] != float("Inf") and dist[vertices.index(u)] + w < dist[vertices.index(v)]:
          print("O grafo possui um ciclo negativo")
          return 0 # break ?

      for i in range(V):
            print("BellmanFord:")
            
            print (("%d" %dist[i]) if dist[i] != "Inf" else  "Inf" ,end=" ")
            if dist[i] != "Inf":
              list_dists.append(dist[i])

            else:
              list_dists.append("Inf")
      print("Nodes", vertices)
      print("pn", previousNode)
      
      for i in range(V):
        if vertices[i] == goal:
         
          parentNode = vertices[i]
          for j in range(V):
            parent = parentNode
            path.append(parentNode)
            parentNode = previousNode[vertices.index(parent)]
            print("parentNode", parentNode)
      
            
            if parentNode == src:
              path.append(parentNode)
              break
            
      path.reverse()
      print("p", path)
      return list_dists, path


    def dijkstra(self, src, goal):
      
      """ !Obsoleto!Executa o algoritmo de dijkstra a partir de uma origem
          Requisito 11

          Returns:
            Uma lista com as menores distancias da origem para todos dos vertices

      """ 
      previousNode = []
      list_dists = []
      path = []
      V = len(self.getVertices())

      vertices = []
      MAX_SIZE = sys.maxsize
      dist = [MAX_SIZE] * V
      previousNode = [0] * V
     
      stack = self.ordTopologica()
      
      vertices = copy.deepcopy(stack)
      print('stack', stack)
      print('Vertices', vertices)
      stack.reverse()
      #vertices.reverse()
      
      dist[vertices.index(src)] = 0
      
      print('stack', stack)
      print('Vertices', vertices)
      print("d", len(stack))

      while stack:
        i = stack.pop()
      
        for node, weight in self.getWeightNNodeFromNode(i):

          print("i", i)
          print("node", node)
          print("weight", weight)
          if dist[vertices.index(node)] > dist[vertices.index(i)] + weight:
                print("ce")
               
                dist[vertices.index(node)] = dist[vertices.index(i)] + weight
                #previousNode[vertices.index(node)] = (i, dist[vertices.index(i)] + weight)
                previousNode[vertices.index(node)] = (i)
      for i in range(V):
            print("Dijkstra:")
            

            print (("%d" %dist[i]) if dist[i] != MAX_SIZE else  "Inf" ,end=" ")
            if dist[i] != MAX_SIZE:
              list_dists.append(dist[i])

            else:
              list_dists.append("Inf")
      print("Nodes", vertices)
      print("pn", previousNode)
      
      for i in range(V):
        if vertices[i] == goal:
         
          parentNode = vertices[i]
          for j in range(V):
            parent = parentNode
            path.append(parentNode)
            parentNode = previousNode[vertices.index(parent)]
            print("parentNode", parentNode)
      
            
            if parentNode == src:
              path.append(parentNode)
              break
            
      path.reverse()
      print("p", path)
      return list_dists, path

    def AGM(self): 
        """Calcula a Árvore Geradora Mínima de um Grafo não-orientado e conexo, utilizando do
        algoritmo de Kluskal.
        1. Ordenar os valores das arestas do grafo;
        2. Enquanto não tiver ciclo, adicionar as arestas em ordem crescente

        Correspondente ao requisito 12.
        """
        if self.conexidadeGrafo and not self.digrafo:
          self.dataframe['label'] = pd.to_numeric(self.dataframe['label'], errors='coerce')
          self.dataframe = self.dataframe.sort_values(by=['label'])
          self.dataframe = self.dataframe.drop_duplicates()
          second_dataframe = Grafo()
          for index, row in self.dataframe.iterrows():
            second_dataframe.dataframe = pd.concat(
              [second_dataframe.dataframe, 
              pd.DataFrame([row], columns=["origem", "destino", "label"])], 
              ignore_index=False
            ) 
            if second_dataframe.hasCiclo():
              second_dataframe.dataframe.drop(index, axis=0, inplace=True)
          self.imagem_bin['agm'] = second_dataframe.createImg()
          

    def createDataFrame(self, text):
        """Cria o DataFrame baseado em um arquivo de texto, permitindo a manipulação do mesmo.

        Args:
          text (String): Texto utilizado para a criação do DataFrame do Grafo, 
          permitindo a manipulação; e, posteriormente, a criação da imagem. 
          Estrurado em lin[0], correspondente ao vértice inicial; lin[1], 
          correspondente  ao vértice final; lin[2], corresponte à label da aresta; 
          lin[3], correspondente ao subgrupo do grafo em questão (cluster).
        """
        dados = text.split("\n")
        for linha in dados:
          lin = linha.split()
          if len(lin) == 4:
            self.__createAresta(lin[0], lin[1], lin[2], lin[3])
          elif len(lin) == 3:
            self.__createAresta(lin[0], lin[1], lin[2])
          elif len(lin) == 2:
            self.__createAresta(lin[0], lin[1])
          elif len(lin) == 1:
            self.__createAresta(lin[0])
        try:
            self.__conversaoDataMatriz()
        except TypeError:
            print("Algum erro no codigo do pedro")

    def createImg(self, ordering=[]):
        """Gera a imagem do grafo em questão, mediante escrita do mesmo no arquivo 
        grafo.txt/grafo_com_sub_grafos.txt, e constrói a imagem correspondente no arquivo
        grafo.png/grafo_com_sub_grafos.png
        
        Args:
          ordering (list): Lista que define a ordem em que os elementos devem ser criados
          e dispostos de forma horizontal na imagem. Caso vazia, os elementos são criados
          na ordem em que foram instanciados para a criação de arestas, e não sao dispostos
          horizontalmente. Importante para a ordenação topológica.
        """
        cores = ["blue", "lightgrey", "red", "pink", "yellow"]
        clusters = len(self.dataframe.cluster.unique())
        if (self.digrafo):
          grafo = Digraph("G", format='png')
        else:
          grafo = Graph("G", format='png')
        if (len(ordering) == 0):
          grafo.attr(shape="circle", rankdir="LR", size="30.0")
        elif (len(ordering) > 0):
          grafo.attr(shape="circle", rankdir="TB", size="30.0", ordering='in', rank='same')
          with grafo.subgraph() as level:
            for node_name in range(0, len(ordering)):
              level.node(ordering[node_name])
            for edge_inv in range(0, len(ordering)-1):
              level.edge(ordering[edge_inv], ordering[edge_inv+1], style='invis')
        if (clusters > 1):
          for cluster in self.dataframe.cluster.unique():
            df = self.dataframe.query("cluster == @cluster")
            with grafo.subgraph(name=f"cluster {cluster}") as c:
              c.attr(color=cores.pop(), label=f"Componente {cluster}")
              for _, row in df.iterrows():
                c.edge(row.origem, row.destino, label=str(row.label))
          grafo.render("grafo/static/images/grafo_com_sub_grafos")
          return b64encode(grafo._repr_image_png()).decode()
        else:
          for _, row in self.dataframe.iterrows():
            verdade = row.isnull()
            if not verdade[1]:
              if not verdade[2]:
                grafo.edge(row.origem, row.destino, str(row.label))
              else:
                grafo.edge(row.origem, row.destino)
            else:
              grafo.node(row.origem)
          grafo.render("grafo/static/images/grafo", overwrite_source=True)
          return b64encode(grafo._repr_image_png()).decode()
          


