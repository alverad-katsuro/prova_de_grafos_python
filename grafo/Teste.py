from strucs.Grafo import Grafo as Grafo

import pandas as pd

data = pd.DataFrame([["R0", "R1", "15", "0"]], columns=["origem", "destino", "label", "cluster"])


grafo = Grafo()
grafo.dataframe = data
grafo.createImg()

