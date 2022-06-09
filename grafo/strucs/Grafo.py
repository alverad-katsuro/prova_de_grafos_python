import pandas as pd
import numpy as np
from graphviz import Digraph, Graph

class Grafo():
  def __init__(self, digrafo = False):
    self.dataframe = pd.DataFrame(columns=["origem", "destino", "label", "cluster"])
    self.digrafo = digrafo

  def createAresta(self, origem, destino, label=np.NAN, cluster=np.NAN):
    self.dataframe.append(pd.DataFrame(columns=["origem", "destino", "label", "cluster"], data=[origem, destino, label, cluster]))

  def createImg(self):
    cores = ["blue", "lightgrey", "red", "pink", "yellow"]
    clusters = len(self.dataframe.cluster.unique())
    if (self.digrafo):
      grafo = Digraph("G", format='png')
    else:
      grafo = Graph("G", format='png')
    grafo.attr(shape="circle", rankdir="LR", size="8,5")
    if (clusters > 1):
      for cluster in range(clusters):
        df = self.dataframe.query("cluster == @cluster")
        print(df)
        with grafo.subgraph(name=f"cluster {cluster}") as c:
          c.attr(color=cores.pop(), label=f"Componente {cluster}")
          for index, row in df.iterrows():
            c.edge(row.origem, row.destino, label=str(row.label))
      grafo.save("grafo/img/grafo_com_sub_grafos")
      grafo.view()
    else:
      for index, row in self.dataframe.iterrows():
          grafo.edge(row.origem, row.destino, str(row.label))
      grafo.save("grafo/img/grafo")
      grafo.view()


