import numpy as np
import pandas as pd
from base64 import b64encode

from graphviz import Digraph, Graph

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
          return (self.__calcVizinhoSucessor(input_name), self.__calcVizinhoAntecessor(input_name))
        else:
          return self.__calcVizinhoGeneric(input_name)

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
              continue
        return viz

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
          if force:
            pass
          pass
        else:
          return self.__conexidadeNotDigrafo()

    def __conexidadeNotDigrafo(self): 
        """Verifica se um grafo não-orientado é conexo ou desconexo.
            
        Returns:
          Verdadeiro, se o grafo for conexo; Falso, se o grafo for desconexo.
        """
        if (self.digrafo == False): #!Bug. A ordem em que os vértices estão dispostos podem enganar o algoritmo
            vertices = []
            goTo = []
            subset = self.dataframe.drop_duplicates(subset=["origem", "destino"], keep='first')
            for _, row in subset.iterrows():
              if row["origem"] not in vertices:
                vertices.append(row["origem"])
              if ((not pd.isnull(row["destino"])) and (row["destino"] not in vertices)):
                vertices.append(row["destino"])
            for loop in range(0, len(vertices)):
              goTo2 = set()  
              for _, row in subset.iterrows():
                if ((vertices[loop] == row["origem"]) and (not pd.isnull(row["destino"]))):
                  goTo2.add(row["destino"])
              goTo.append(goTo2)  
              print(self.calcAdjacencia(vertices[loop]), goTo2)
            print(goTo)
            for i in range(0, len(goTo)): 
              for j in range(i+1, len(goTo)):
                if (len(goTo[i].intersection(goTo[j])) != 0):
                  return True
            return False

    def hasCiclo(self):
        """Verifica se um grafo possui algum ciclo.
            Requisito 8

        Returns:
          Verdadeiro, caso possua ciclo; Falso, caso não possua ciclo.
        """
        if self.digrafo:
          return self.buscaProfundidade001(identify_cycle=True)
        else:
          return self.buscaProfundidade002(identify_cycle=True)
        

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
      # conjunto_vertices = self.getVertices() - used
        #print(conjunto_vertices)
        #print(used,'\n')
        #conjunto_vertices_utilizados = []
        conjunto_vertices = self.getVertices()
        used = []
        adjacencia = set()
        order = []
        done = []
        element1 = 0
        #element1 = conjunto_vertices.pop()
        #print("starts at", element1)
        #adjacencia2 = self.__calcVizinhoSucessor(element1) - set(element1)
        if (self.digrafo):
          count = len(conjunto_vertices)
          while (count != len(done)):
            """if identify_cycle:
              for _, row in self.dataframe.iterrows():
                if ((row["origem"] == element) and (row["destino"] in conjunto2)):
                  return True
              return False"""
            print('original', conjunto_vertices)
            print('queue', order)
            print('cortados/preto', done)
            if (len(order) == 0):
              element1 = conjunto_vertices.pop()
              print('new_choice: ', element1)
              if element1 not in used:
                used.append(element1)
            else: 
              element1 = order.pop()
              print('new_choice: ', element1)
              if element1 not in used:
                used.insert(len(used), element1)
              if element1 in conjunto_vertices:
                conjunto_vertices.remove(element1)
            print(element1)
            adjacencia = self.__calcVizinhoSucessor(element1) - set([element1])
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
          #  order.reverse()
          # conjunto_vertices.insert(0, element1)
            adjacencia = set()

          if (identify_cycle):
            return False
          print('used: ', used)
          print('done: ', done)

          done.reverse()

          return done
              #conjunto_vertices_utilizados.append(element)
              # conjunto_vertices.remove(element1)

    def buscaProfundidade002(self, identify_cycle=False):
        """Verifica se um grafo (não-orientado) possui algum ciclo através de 
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
        # conjunto_vertices = self.getVertices() - used
        #print(conjunto_vertices)
        #print(used,'\n')
        #conjunto_vertices_utilizados = []
        conjunto_vertices = self.getVertices()
        used = []
        adj = []
        adjacencia = []
        order = []
        done = []
        element1 = 0
        #element1 = conjunto_vertices.pop()
        #print("starts at", element1)
        #adjacencia2 = self.__calcVizinhoSucessor(element1) - set(element1)
        if (self.digrafo == False):
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
            #  print("i am at", element)
              if ((element in conjunto_vertices) or (element not in order)):
                order.append(element)
              else:
                print(f'element {element} was already visited!')
          #  order.reverse()
          # conjunto_vertices.insert(0, element1)
            adjacencia = []

          if identify_cycle:
            return False
          print('used: ', used)
          print('done: ', done)

          done.reverse()

          return done

    def ordenacaoTopologica(self): 
        """Calcula a ordenação topológica de um grafo orientado, acíclico e conexo,
        e gera a imagem do mesmo.

        Correspondente ao requisito 9.
        """        
<<<<<<< HEAD
        if self.digrafo and not self.buscaProfundidade001(identify_cycle=True):
=======
        if self.digrafo:# and self.conexidadeGrafo() and not self.buscaProfundidade001(identify_cycle=True):
>>>>>>> 19dd260c51f0487fa852433eb7cb222cba2843cc
          list_order = self.buscaProfundidade001()
          print(list_order)
          novo_grafo = Grafo()
          novo_grafo.dataframe = self.dataframe
          novo_grafo.createImg(ordering=list_order)
          self.imagem_bin["topologica"] = b64encode(novo_grafo.imagem_bin).decode()



    def AGM(self): 
        """Calcula a Árvore Geradora Mínima de um Grafo não-orientado e conexo, utilizando do
        algoritmo de Kluskal.
        1. Ordenar os valores das arestas do grafo;
        2. Enquanto não tiver ciclo, adicionar as arestas em ordem crescente

        Correspondente ao requisito 12.
        """
        if (self.digrafo == False): #!Incompleto. Não confere a conexidade
          self.dataframe['label'] = pd.to_numeric(self.dataframe['label'], errors='coerce')#.values.all()
          self.dataframe = self.dataframe.sort_values(by=['label'])
          self.dataframe = self.dataframe.drop_duplicates()
          second_dataframe = Grafo()
          for index, row in self.dataframe.iterrows():
            second_dataframe.dataframe = pd.concat(
              [second_dataframe.dataframe, 
              pd.DataFrame([row], columns=["origem", "destino", "label"])], 
              ignore_index=False
            ) 
            #print(second_dataframe.dataframe)   
            if second_dataframe.hasCiclo():
              #sleep(10)
              second_dataframe.dataframe.drop(index, axis=0, inplace=True)
          #print(second_dataframe.dataframe)
          #text = second_dataframe.dataframe[:].to_string(header=False, index=False).replace('NaN', '')
          #print(text)
          #second_dataframe.createDataFrame(text)
          second_dataframe.createImg()
          self.imagem_bin["agm"] = b64encode(second_dataframe.imagem_bin).decode()


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
          grafo.attr(shape="circle", rankdir="LR", size="8,5")
        elif (len(ordering) > 0):
          grafo.attr(shape="circle", rankdir="TB", size="8,5", ordering='in', rank='same')
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
          self.imagem_bin["grafo"] = b64encode(grafo._repr_image_png()).decode()
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
          self.imagem_bin["grafo"] = b64encode(grafo._repr_image_png()).decode()
          


