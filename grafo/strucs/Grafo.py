import pandas as pd
import numpy as np

from graphviz import Digraph, Graph

class Grafo():
  def __init__(self, digrafo = False):
    self.dataframe = pd.DataFrame(columns=["origem", "destino", "label", "cluster"])
    self.digrafo = digrafo
    self.log = []
    self.imagem_bin = None

  def hasAresta(self): 
    #Requisito 1: Verificar a existencia de uma aresta.
    return False if (self.dataframe["destino"].isnull().values.all()) else True

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
      return (self.calcVizinhoSucessor(input_name), self.calcVizinhoAntecessor(input_name))
    else:
      return self.calcVizinhoGeneric(input_name)

  def calcVizinhoGeneric(self, input_name): 
    #Requisito 3: Informar a adjacencia de um vértice (Not Digrafo).
    viz = {}
    for _, row in self.dataframe.iterrows():
      if (row["origem"] == input_name):
        viz.add(row["destino"])
      elif (row["destino"] == input_name):
        viz.add(row["origem"])
      else:
        continue
    if (len(viz) > 0):
      viz.append(input_name)
    return viz

  def calcVizinhoSucessor(self, input_name): 
    #Requisito 3: Informar a adjacencia de um vertice (Digrafo)
    viz = {}
    for _, row in self.dataframe.iterrows():
      if (row["origem"] == input_name):
        viz.add(row["destino"])
      else:
        continue
    if (len(viz) > 0):
      viz.append(input_name)
    return viz

  def calcVizinhoAntecessor(self, input_name): 
    #Requisito 3: Informar a adjacencia de um vertice. (Digrafo)
    if (self.digrafo == True):
      return (self.calcVizinhoSucessor(input_name), self.calcVizinhoAntecessor(input_name))
    else:
      viz = set()
      for _, row in self.dataframe.iterrows():
        if (row["destino"] == input_name):
          viz.add(row["origem"])
        else:
          continue
      if (len(viz) > 0):
        viz.append(input_name)
      return viz

  def conexidadeNotDigrafo(self): 
    #4. Verificar se um grafo não-orientado é conexo.
    if (self.digrafo == False):
      vertices_conexo = set()
      vertices_desconexo = set()
      for _, row in self.dataframe.iterrows():
        if not (pd.isnull(row["destino"])):
          vertices_conexo.add(row["origem"])
          vertices_conexo.add(row["destino"])
        else:
          vertices_desconexo.add(row["origem"])
      return True if vertices_conexo.issuperset(vertices_desconexo) else False  
      

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


