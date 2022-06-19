import pandas as pd
import numpy as np
from time import sleep


from graphviz import Digraph, Graph

from strucs.Vertice import Vertice as Vertice

class Grafo():
  def __init__(self, digrafo = False):
    self.dataframe = pd.DataFrame(columns=["origem", "destino", "label", "cluster"])
    self.digrafo = digrafo
    self.log = []
    self.imagem_bin = None


  def getVertices(self):
    vertices = set()
    for _, row in self.dataframe.iterrows():
      if (not pd.isnull(row["destino"])):
        vertices.add(row["origem"]) 
        vertices.add(row["destino"]) 
   # print(vertices)
    return vertices

  def containsAresta(self, *args):
    if len(args) == 0:
      return self.__hasAresta1()
    elif len(args) == 1 and isinstance(args[0], str):
      return self.__hasAresta2(args[0])
    elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
      return self.__hasAresta3(args[0], args[1])
    else:
      pass

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
    #Requisito 2: Informar o grau de um vertice.
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

  def calcAdjacencia(self, input_name): 
    #Requisito 3: Informar a adjacencia de um vertice.
    if (self.digrafo == True):
      return (self.__calcVizinhoSucessor(input_name), self.__calcVizinhoAntecessor(input_name))
    else:
      return self.__calcVizinhoGeneric(input_name)

  def __calcVizinhoGeneric(self, input_name): 
    #Requisito 3: Informar a adjacencia de um vértice (Not Digrafo).
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
    #Requisito 3: Informar a adjacencia de um vertice (Digrafo)
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
    #Requisito 3: Informar a adjacencia de um vertice. (Digrafo)
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

  def conexidadeNotDigrafo(self): 
    #4. Verificar se um grafo não-orientado é conexo.
    if (self.digrafo == False):
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
      for i in range(0, len(goTo)): 
        for j in range(i+1, len(goTo)):
          if (len(goTo[i].intersection(goTo[j])) != 0):
            return True
      return False

  def hasCiclo(self):
    if self.digrafo:
      return self.buscaProfundidade001(identify_cycle=True)
    else:
      return self.buscaProfundidade002(identify_cycle=True)
      

  def buscaProfundidade001(self, identify_cycle=False):
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

        adjacencia = self.__calcVizinhoSucessor(element1) - set(element1)
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

      if (identify_cycle):
        return False
      print('used: ', used)
      print('done: ', done)

      done.reverse()

      return done

    """def grafoTransposto(self):
    #pros componentes fortemente conexos
    for _, row in self.dataframe.iterrows():
      if (not pd.isnull(row["destino"])):
        x = row['origem']
        row['origem'] = row['destino']
        row['destino'] = x"""

  def ordenacaoTopologica(self): 
    #Requisito 9: Dado um dı́grafo acı́clico e conexo, informar uma ordenação topológica presente no dı́grafo
    if (self.digrafo == True):

      list_order = self.buscaProfundidade001()
      print(list_order)
      self.createImg(ordering=list_order)

  def AGM(self): 
    #Requisito 12: Encontrar uma arvore geradora minima de um grafo nao-orientado e conexo.
    if (self.digrafo == False):
      self.dataframe['label'] = pd.to_numeric(self.dataframe['label'], errors='coerce')#.values.all()
      self.dataframe = self.dataframe.sort_values(by=['label'])
      self.dataframe = self.dataframe.drop_duplicates()
      second_dataframe = Grafo()
      for index, row in self.dataframe.iterrows():
        second_dataframe.dataframe = pd.concat([second_dataframe.dataframe, pd.DataFrame([row], columns=["origem", "destino", "label"])], ignore_index=False) 
        print(second_dataframe.dataframe)   
        if second_dataframe.hasCiclo():
          #sleep(10)
          second_dataframe.dataframe.drop(index, axis=0, inplace=True)
      print(second_dataframe.dataframe)
      text = second_dataframe.dataframe[:].to_string(header=False, index=False).replace('NaN', '')
      print(text)
      #second_dataframe.createDataFrame(text)
      second_dataframe.createImg()

  def createAresta(self, origem, destino=np.nan, label=np.nan, cluster=np.nan):
    if len(self.dataframe.query("(origem == @origem) & (destino == @destino) & (label == @label) & (cluster == @cluster)")) == 0:
      self.dataframe = pd.concat([self.dataframe, pd.DataFrame([[origem, destino, label, cluster]], columns=["origem", "destino", "label", "cluster"])], ignore_index=True)

  def createDataFrame(self, text):
    dados = text.split("\n")
    for linha in dados:
      lin = linha.split()
      if len(lin) == 4:
        self.createAresta(lin[0], lin[1], lin[2], lin[3])
      elif len(lin) == 3:
        self.createAresta(lin[0], lin[1], lin[2])
      elif len(lin) == 2:
        self.createAresta(lin[0], lin[1])
      elif len(lin) == 1:
        self.createAresta(lin[0])

  def createImg(self, ordering=[]):
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
      self.imagem_bin = grafo._repr_image_png()
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
      self.imagem_bin = grafo._repr_image_png()


