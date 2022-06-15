import pandas as pd
import numpy as np

from graphviz import Digraph, Graph

class Grafo():
  def __init__(self, digrafo = False):
    self.dataframe = pd.DataFrame(columns=["origem", "destino", "label", "cluster"])
    self.digrafo = digrafo
    self.log = []
    self.imagem_bin = None

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
      

  def buscaProfundidade(self):
    pass
    
  def ordenacaoTopologica(self): 
    #Requisito 9: Dado um dı́grafo acı́clico e conexo, informar uma ordenação topológica presente no dı́grafo
    if (self.digrafo == True):
      order = self.buscaEmProfundidade()
      for element in order:
        print(element)
      

  def displayInteger(self):
    pass
  

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

  def createImg(self):
    cores = ["blue", "lightgrey", "red", "pink", "yellow"]
    clusters = len(self.dataframe.cluster.unique())
    if (self.digrafo):
      grafo = Digraph("G", format='png')
    else:
      grafo = Graph("G", format='png')
    grafo.attr(shape="circle", rankdir="LR", size="8,5")
    if (clusters > 1):
      for cluster in self.dataframe.cluster.unique():
        df = self.dataframe.query("cluster == @cluster")
        with grafo.subgraph(name=f"cluster {cluster}") as c:
          c.attr(color=cores.pop(), label=f"Componente {cluster}")
          for index, row in df.iterrows():
            c.edge(row.origem, row.destino, label=str(row.label))
      grafo.render("grafo/static/images/grafo_com_sub_grafos")
      self.imagem_bin = grafo._repr_image_png()
    else:
      for index, row in self.dataframe.iterrows():
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


