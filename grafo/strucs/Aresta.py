class Aresta():
  def __init__(self, origem, destino=None):
    self.origem = origem
    self.destino = destino

  def __str__(self) -> str:
      return f"{self.origem} -> {self.destino}"