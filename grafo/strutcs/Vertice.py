class Vertice():
  def __init__(self, nome, arestas=[]):
    self.nome = nome
    self.arestas = arestas
  
  def __str__(self) -> str:
    return self.nome
    