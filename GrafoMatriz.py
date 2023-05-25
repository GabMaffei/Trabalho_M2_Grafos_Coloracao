from Grafos import Grafos


class GrafoMatriz(Grafos):
    def __init__(self, direcionado=False, ponderado=False):
        super().__init__(direcionado, ponderado)
        self.matriz = list()
        self.labels = dict()  # Contém os nomes de vértices

    def __str__(self):  # imprimeGrafo
        return (str(self.matriz))

    def _balanceamentoVerticeRemover(self, idVertice):
        # Ajusta o comprimento do vértice, após remoções
        matrizTmp = list()
        for verticeAtual in self.matriz:
            verticeTmp = list()
            for idx, aresta in enumerate(verticeAtual):
                if idx == idVertice:
                    continue
                verticeTmp.append(aresta)
            matrizTmp.append(verticeTmp)
        self.matriz = matrizTmp

    def _balanceamentoMatriz(self):
        # Ajusta o comprimento da matriz
        arestasDaVerticeAtual = list()
        for vertice in range(self.vertices - 1):
            arestasDaVerticeAtual = self.matriz[vertice]
            arestasDaVerticeAtual.append([0, 0])
            self.matriz[vertice] = arestasDaVerticeAtual

    def inserirVertice(self, label):
        # Adiciona um vértice sem nenhuma aresta associada a ele, pode parecer
        # igual em ambos os casos, mas não é.
        # Precisamos adicionar esse vértice no vetor de vértices e também alocar
        # seu espaço para as arestas.

        # Define nome da vértice
        self.labels[label] = self.vertices
        self.vertices += 1

        # Cria linha com arestas para a nova vértice
        arestasDaVerticeAtual = list()

        for vertice in range(self.vertices):
            arestasDaVerticeAtual.append([0, 0])

        self.matriz.append(arestasDaVerticeAtual)

        if self.vertices > 1:
            self._balanceamentoMatriz()

    def removerVertice(self, label):
        # Remove um vértice do grafo, elimina a linha e coluna dele da matriz e a
        # referência dele da lista, junto com todas as arestas que chegam e saem
        # dele.
        # Converte o indice para label
        if isinstance(label, int):
            label = self.labelVertice(label)

        # Removendo o label
        idVertice = self.labels.get(label)
        self.labels.pop(label)
        # Balanceando os labels
        labelsTmp = dict()
        count = 0
        for label in self.labels.items():
            labelsTmp[label[0]] = count
            count += 1
        self.labels = labelsTmp
        # Diminuindo o número de vértices
        self.vertices -= 1

        matrizTmp = list()
        for vertice in range(self.vertices + 1):
            if vertice == idVertice:
                continue
            matrizTmp.append(self.matriz[vertice])

        self.matriz = matrizTmp

        # Balanceamento Negativo
        self._balanceamentoVerticeRemover(idVertice)

    def labelVertice(self, indice):
        # Funções básicas para retornar o nome de um vértice.
        # return str(self.labels.get(indice))
        label = [k for k, v in self.labels.items() if v == indice]
        return (label[0])

    def imprimeGrafo(self):
        # Imprimir o grafo no console, tentem deixar próximo da representação
        # dos slides (não precisa da grade da matriz).
        print('Grafo:')
        print('   ' + str(list(range(len(self.matriz)))))
        for idx, vertice in enumerate(self.matriz):
            print(str(idx) + ': ' + str(vertice))

    def inserirAresta(self, origem, destino, peso=1):
        # Essa operação deve ter um cuidado especial,
        # ela deve ser executada levando em conta o tipo do grafo.
        # No caso de um grafo ponderado o peso deve ser aplicado e
        # no caso de um grafo direcionado, uma ligação de volta deve ser adicionada;

        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)
        # Se não ponderado, o peso é igual a 1
        if not self.ponderado:
            peso = 1

        # Adiciona a ligação
        arestaTmp = list()
        for idx, aresta in enumerate(self.matriz[origem]):
            if idx == destino:
                arestaTmp.append([1, peso])
                continue
            arestaTmp.append(aresta)
        self.matriz[origem] = arestaTmp

        # Se direcionado, adiciona a ligação de volta
        if self.direcionado:
            arestaTmp = list()
            for idx, aresta in enumerate(self.matriz[destino]):
                if idx == origem:
                    arestaTmp.append([1, peso])
                    continue
                arestaTmp.append(aresta)
            self.matriz[destino] = arestaTmp

    def removerAresta(self, origem, destino):
        # Remove uma aresta entre dois vértices no grafo, lembrando
        # que no grafo não direcionado deve ser removida a aresta de retorno também;
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)

        # Remove a ligação
        arestaTmp = list()
        for idx, aresta in enumerate(self.matriz[origem]):
            if idx == destino:
                arestaTmp.append([0, 0])
                continue
            arestaTmp.append(aresta)
        self.matriz[origem] = arestaTmp

        # Se direcionado, remove a ligação de volta
        if self.direcionado:
            arestaTmp = list()
            for idx, aresta in enumerate(self.matriz[destino]):
                if idx == origem:
                    arestaTmp.append([0, 0])
                    continue
                arestaTmp.append(aresta)
            self.matriz[destino] = arestaTmp

    def existeAresta(self, origem, destino):
        # Verifica a existência de uma aresta, aqui vemos uma diferença
        # grande entre matriz e lista.
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)

        # for idx, aresta in enumerate(self.matriz[origem]):
        #  if idx == destino and aresta[0] == 1:
        #    return True

        if self.matriz[origem][destino][0] == 1:
            return True

        return False

    def pesoAresta(self, origem, destino):
        # Retorne o peso de uma aresta, aqui vemos uma diferença
        # grande entre matriz e lista.
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)

        if self.ponderado == False:
            return 0

        for idx, aresta in enumerate(self.matriz[origem]):
            if idx == destino:
                return aresta[1]

        return 0

    def retornarVizinhos(self, vertice):
        # Função para retorno dos vizinhos de um vértice, necessária pois não
        # teremos acesso a estrutura das arestas para os próximos algoritmos.
        # Converte os labels para indices
        if isinstance(vertice, str):
            vertice = self.labels.get(vertice)

        # Só verifica os vizinhos da vértice, ou seja, não verifica se existem
        # arestas ligadas a vértice atual com origem em outras vértices
        # Dúvida: preciso retornar os antecessores?
        # https://www.inf.ufsc.br/grafos/definicoes/definicao.html#:~:text=ADJAC%C3%8ANCIA,de%20Antonio.
        vizinhosIdx = list()
        for idx, aresta in enumerate(self.matriz[vertice]):
            if aresta[0] == 1:
                tuplaTemp = (self.labelVertice(idx), idx)
                vizinhosIdx.append(tuplaTemp)
        return vizinhosIdx


'''
grafoExemplo = GrafoMatriz(direcionado = False, ponderado = False)
grafoExemplo.inserirVertice('um')
grafoExemplo.inserirVertice('dois')
grafoExemplo.inserirVertice('tres')
# print(grafoExemplo)

# print(grafoExemplo.labelVertice(0))
# print(grafoExemplo.labelVertice(1))

# print(grafoExemplo)

# print(grafoExemplo.labelVertice(0))
# print(grafoExemplo.labelVertice(1))

grafoExemplo.imprimeGrafo()

grafoExemplo.inserirAresta(0, 1)
grafoExemplo.removerVertice('tres')
grafoExemplo.imprimeGrafo()
print(grafoExemplo.existeAresta(0, 1))
print(grafoExemplo.existeAresta(1, 0))
# print(grafoExemplo.pesoAresta(0, 1))
# print(grafoExemplo.pesoAresta(1, 0))
print(grafoExemplo.retornarVizinhos(0))
print(grafoExemplo.retornarVizinhos(1))

grafoExemplo.removerAresta(0, 1)
grafoExemplo.imprimeGrafo()
# print(grafoExemplo.existeAresta(0, 1))
# print(grafoExemplo.existeAresta(1, 0))
# print(grafoExemplo.pesoAresta(0, 1))
# print(grafoExemplo.pesoAresta(1, 0))
print(grafoExemplo.retornarVizinhos(0))
print(grafoExemplo.retornarVizinhos(1))
'''
