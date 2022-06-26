import networkx as nx


class Grafo_class:
    """ Grafo utilizando lista de adjacencia. """

    tempo = 0
    INFINITO = float("inf")

    def __init__(self, vertices): 
        self.qtd_vertices = vertices
        self.lista_adjacente = [[] for _ in range(self.qtd_vertices)]
        self.lista_articulacoes = []
        self.grau = [0] * self.qtd_vertices  # Grau dos vertices
        self.vertices = set()
        self.vertices_de_grau_impar = []
    
    def inserir(self, u, w):
        self.lista_adjacente[u].append(w)
        self.lista_adjacente[w].append(u)
        self.grau[u] += 1
        self.grau[w] += 1
    
    def remover(self, u, w):
        self.lista_adjacente[u].remove(w)
        self.lista_adjacente[w].remove(u)
        self.grau[u] -= 1
        self.grau[w] -= 1 

    def pontos_de_articulacoes(self):
        """
        Retorna os vértices que são pontos de articulações do grafo.
        Um vértice é ponto de articulação se:
        - Se pai[v] == −1 (v é a raíz da árvore DFS) e v tem pelo menos dois filhos na árvore DFS.
        - Se pai[v] != −1 (v não é raiz da árvore no DFS) e v tem pelo menos um filho w tal que nenhum
          descendente na sub-árvore(w) está conectado a algum ancestral de v usando aresta de retorno.
        Usando o vetor low (lowest preorder number):
        - Uma aresta {v, w} identifica o ponto de articulação v se pai[v] != nulo e low[w] >= pre[v].
        """

        Grafo_class.tempo = 0
        pre = [-1] * self.qtd_vertices
        pai = [-1] * self.qtd_vertices
        low = [Grafo_class.INFINITO] * self.qtd_vertices

        self.DFS(0, pre, pai, low)  # Assumindo que o grafo é conexo (começa o DFS do vértice 0)
        if(self.qtd_vertices <= 2):
              a = "Este grafo não é biconexo pois a quantidade de vértices é <= 2 !!!"
              return a, self.lista_articulacoes
        elif(len(self.lista_articulacoes) == 0):
              a = ("Então ele é biconexo, pois é necessário tirar no mínimo duas arestas para tornar o mesmo DESCONEXO!!!")
              return a, self.lista_articulacoes
        else:
              a = ("\nEste grafo não é biconexo pois ele possui os seguintes pontos de articulação: ")
              return a, self.lista_articulacoes

    def DFS(self, vertice, pre, pai, low):
        Grafo_class.tempo += 1
        pre[vertice] = Grafo_class.tempo
        low[vertice] = Grafo_class.tempo
        eh_ponto_de_articulacao = False
        filhos = 0

        for w in self.lista_adjacente[vertice]:
            if pre[w] == -1:  # Aresta de arborescencia
                pai[w] = vertice
                filhos += 1
                self.DFS(w, pre, pai, low)
                
                low[vertice] = min(low[vertice], low[w])

                if low[w] >= pre[vertice]:
                    eh_ponto_de_articulacao = True
                
            elif w != pai[vertice]:  # Aresta de retorno
                low[vertice] = min(low[vertice], pre[w])
        
        if (pai[vertice] != -1 and eh_ponto_de_articulacao) or (pai[vertice] == -1 and filhos > 1):
            self.lista_articulacoes.append(vertice)

    def fleury(self):
        """
        O problema do carteiro chinês pode ser resolvido pelo Algoritmo de Fleury, já que ele encontra
        uma trilha de Euler no grafo euleriano. Este algoritmo constrói uma trilha sujeita à condição
        de que, em cada passo, a aresta escolhida para compor a trilha não seja de corte no grafo 
        restante, a menos que não haja alternativa. Algoritmo detalhado em 'Aula 14 > Algoritmo de Fleury.md'
        """
        if len(self.vertices_de_grau_impar) > 2:
            return []
        
        if len(self.vertices_de_grau_impar) == 0:  # Trilha euleriana fechada
            vertice = 0  # Começa pelo vértice 0
        else:
            vertice = self.vertices_de_grau_impar[0]  # Trilha euleriana aberta

        for u in range(self.qtd_vertices):
            self.vertices.add(u)

        trilha = []  
        self.trilha_euleriana(vertice, trilha)
        return trilha

    def trilha_euleriana(self, vertice, trilha):
        trilha.append(vertice)

        if len(self.lista_adjacente[vertice]) == 0:
            return

        for w in self.lista_adjacente[vertice]:
            if not self.eh_ponte(vertice, w):
                self.remover(vertice, w)
                

                if self.grau[vertice] == 0:
                    self.vertices.remove(vertice)
                
                if self.grau[w] == 0:
                    if len(self.vertices) > 0:
                      self.vertices.remove(w)

                self.trilha_euleriana(w, trilha)
                return 

    def eh_ponte(self, u, v):
        if len(self.lista_adjacente[u]) == 1:
            return False
        
        self.remover(u, v)

        if not self.eh_conexo():
            resultado = True
        else:
            resultado = False

        self.inserir(u, v)
        return resultado

    def eh_conexo(self):
        visitados = [False] * self.qtd_vertices
        componentes = 0

        for vertice in self.vertices:
            if not visitados[vertice]:
                pilha = [vertice]
                visitados[vertice] = True
                componentes += 1

                while len(pilha) > 0:
                    u = pilha.pop()
                    
                    for w in self.lista_adjacente[u]: # Visita todos os filhos do vértice tirado da pilha
                        if not visitados[w]:
                            pilha.append(w)
                            visitados[w] = True

        return componentes == 1

    def eh_euleriano(self):

        #verificando os vértices de grau ímpar
        cont = 0
        for vertice in self.grau:
            if vertice % 2 == 1:
                self.vertices_de_grau_impar.append(cont)
            cont += 1

        """ Um grafo tem uma trilha euleriana se exatamente 2 vértices de grau ímpar. """
        print('\n')
        if(len(self.vertices_de_grau_impar) == 0):
            return ('O grafo é euleriano!!! Ciclo euleriano encontrado pelo algoritmo de Fleury: ')
        elif(len(self.vertices_de_grau_impar) == 2):
            return ('O grafo é semi-euleriano!!! Trilha euleriano encontrado pelo algoritmo de Fleury: ')
        elif(len(self.vertices_de_grau_impar) > 2):
            return ('O grafo não é euleriano e nem semi-euleriano!!!')

    def eh_planar(self, grafo):
        print('\n')
        g = nx.Graph(grafo) #criar grafo
        g = nx.check_planarity(g) #verificar planaridade atráves do teorema de kuratowski

        #exibição do resultado da verificação da planaridade
        if(g[0]):
            return ("O grafo é planar!!!")
        else:
            return ("O grafo não é planar!!!")

def req10(dataframe):
    arestas = dataframe.iloc[:,:2].values.tolist()
    retornos = {}

    #objetos usados para adaptar os tipos de dados dos vértices com os tipos de dados que são aceitos nas funções
    arestas_conversion = []
    arestas_to_number = {}
    arestas_to_number_reverse = {}


    #adaptar os tipos e nomes dos vértices para ficarem de acordo com as funções
    cont = 0
    for i in arestas:
        if(i[0] not in arestas_to_number):
            arestas_to_number[i[0]] = cont
            cont += 1

        if(i[1] not in arestas_to_number):
            arestas_to_number[i[1]] = cont
            cont += 1

    for key, value in arestas_to_number.items():
        arestas_to_number_reverse[value] = key

    for i in arestas:
        arestas_conversion.append([arestas_to_number[i[0]], arestas_to_number[i[1]]])


    grafo = Grafo_class(len(arestas_to_number.keys())) #informar a quantidade de vértices do grafo

    #adicionar as arestas no grafo
    for aresta in arestas_conversion:
        grafo.inserir(aresta[0], aresta[1])


    #-> Biconexo <-
    #resultado grafo biconexo
    resultado_temp = grafo.pontos_de_articulacoes()
    resultado = resultado_temp[1]
    retornos["biconexo"] = resultado_temp

    #retornos["pontos_articulacoes"] = (f"{' | '.join(str(i) for i in resultado)}")
    #retirando as adaptações que ocorreram acima
    for i in range(0, len(resultado)):
        resultado[i] = arestas_to_number_reverse[resultado[i]]

    #imprimindo os pontos de articulações
    if(len(resultado) != 0):
        retornos["pontos_articulacoes"] = (f"{' | '.join(str(i) for i in resultado)}")
   

    #-> Euleriano <-
    #função para verificar se o grafo é euleriano
    retornos['euleriano'] = grafo.eh_euleriano()

    #obtendo o possível caminho euleriano
    resultado = grafo.fleury()

    #retirando as adaptações que ocorreram acima
    for i in range(0, len(resultado)):
        resultado[i] = arestas_to_number_reverse[resultado[i]]

    #imprimindo o caminho euleriano
    if(len(resultado) != 0):
        retornos["caminho_euleriano"] = (f"{' | '.join(str(i) for i in resultado)}")
        #print(f"{' -> '.join(str(i) for i in resultado)}")


    #-> Planar <-
    #verificando se o grafo é planar
    retornos["planar?"] = grafo.eh_planar(arestas)

    return retornos