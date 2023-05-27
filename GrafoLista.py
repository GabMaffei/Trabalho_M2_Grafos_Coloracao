# from typing_extensions import Self
from operator import itemgetter
from queue import PriorityQueue
import time

from Grafos import Grafos


class GrafoLista(Grafos):

    def __init__(self, direcionado=False, ponderado=False):
        super().__init__(direcionado,
                         ponderado)  # Direcionado = False significa que é direcionado, e True que não é Direcionado
        self.lista = list()
        self.labels = dict()  # Contém os nomes de vértices
        self.dictCores = dict()  # Contém os labels e sua cor correspondente

        self.vertices = 0
        self.arestas = 0
        self.cores = 0  # EM REVISÃO: Tem uma cor / Cada cor aumenta em 1 esse número, e adiciona a cor correspondente ao número anterior
        self.listaCores = list()
        # Exemplo: cores = 3, existem 4 cores, sendo 0,1,2,3

    def __str__(self):
        return str(self.lista)

    def openFile(self, filename):
        if self.vertices != 0 or self.arestas != 0:
            raise Exception('A instância do objeto GrafoLista não está vazia.')

        with open(filename, 'r') as arquivo:
            verticesArquivo, arestasArquivo, direcionadoArquivo, ponderadoArquivo = (arquivo.readline()).split()
            # Checa se é direcionado
            if int(direcionadoArquivo) == 1:
                self.direcionado = False
            else:
                self.direcionado = True
            # Checa se é ponderado
            if int(ponderadoArquivo) == 1:
                self.ponderado = True
            else:
                self.ponderado = False

            for vertice in range(int(verticesArquivo)):
                self.inserirVertice(str(vertice))

            try:

                if self.ponderado:
                    for aresta in range(int(arestasArquivo)):
                        origem, destino, peso = (arquivo.readline()).split()
                        self.inserirAresta(origem, destino, float(peso))
                else:
                    for aresta in range(int(arestasArquivo)):
                        origem, destino = (arquivo.readline()).split()
                        self.inserirAresta(origem, destino)

            except Exception:
                print('Linha vazia, ou com erros. Número de vértices lidas:', len(self.lista))

    def buscaProfunda(self, origem, destino):
        caminho = []
        visitado = set()
        return self._buscaProfunda(origem, destino, caminho, visitado)

    def _buscaProfunda(self, origem, destino, caminho=[], visitado=set()):
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)
        caminho.append(origem)
        visitado.add(origem)

        if origem == destino:
            return caminho
        for (vizinho, peso) in self.lista[origem]:
            if vizinho not in visitado:
                resultado = self._buscaProfunda(vizinho, destino, caminho, visitado)
                if resultado is not None:
                    return resultado
        # caminho.pop() #diferença entre o visitado e o caminho, sem o pop, ele é igual a ordem visitada
        return None

    def buscaLargura(self, origem, destino, validaDestinoAntes=True, visitadoDebug=False):
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)

        visitados = [origem]
        fila = [origem]

        while len(fila) > 0:
            # print('Laço de repetição!')
            verticeAtual = fila.pop()

            if verticeAtual == destino:
                # print('verticeAtual == destino' + str(verticeAtual) + str(destino), sep=';')
                if verticeAtual not in visitados:
                    visitados.append(verticeAtual)
                return visitados

            vizinhos = self.retornarVizinhos(verticeAtual)
            # print('VerticeAtual: ' + str(verticeAtual), end=' ')
            # print('Vizinhos: ' + str(vizinhos))

            for verticeVizinha in vizinhos:
                idxVerticeVizinha = self.labels.get(verticeVizinha[0])
                # print('idxVerticeVizinha: ' + str(idxVerticeVizinha))
                if idxVerticeVizinha not in visitados:
                    fila.append(idxVerticeVizinha)
                    visitados.append(idxVerticeVizinha)
                    if idxVerticeVizinha == destino and validaDestinoAntes:
                        return visitados

            # print('Fila: ' + str(fila), end=' ')
            # print('Visitados: ' + str(visitados))
            # print('Length Fila: ' + str(len(fila)))

        if visitadoDebug:
            return visitados
        return None

    def buscaDijkstra(self, origem, destino):
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)

        caminhosMaisCurtos = self.dijkstra(origem)
        return caminhosMaisCurtos[destino]

    def dijkstra(self, origem):
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)

        caminhosMaisCurtos = {vertice: float('inf') for vertice in range(self.vertices)}
        caminhosMaisCurtos[origem] = 0
        # print('caminhosMaisCurtos inicial:', caminhosMaisCurtos)

        fila = PriorityQueue()
        fila.put((0, origem))
        # print('Fila inicial:', fila.queue)
        visitado = list()

        while not fila.empty():
            (distanciaAtual, verticeAtual) = fila.get()
            visitado.append(verticeAtual)

            vizinhos = self.retornarVizinhos(verticeAtual)
            # print('Vizinhos:', vizinhos)
            # print('Fila loop:', fila.queue)
            for vizinho in vizinhos:
                # print('verticeAtual:', verticeAtual, end=' ')
                # print('VizinhoAtual:', vizinho, end=' ')
                distanciaVizinho = self.pesoArestaLabel(verticeAtual, vizinho[1])
                # print('distanciaVizinhoAtual:', distanciaVizinho)
                if vizinho not in visitado:
                    custoAntigo = caminhosMaisCurtos[self.labels.get(vizinho[0])]
                    custoNovo = caminhosMaisCurtos[verticeAtual] + distanciaVizinho
                    if custoNovo < custoAntigo:
                        fila.put((custoNovo, self.labels.get(vizinho[0])))
                        caminhosMaisCurtos[self.labels.get(vizinho[0])] = custoNovo

        return caminhosMaisCurtos

    def _ordernarArestasDoVertice(self):
        for verticeId in range(len(self.lista)):
            self.lista[verticeId].sort(key=itemgetter(0))

    def inserirVertice(self, label):
        # Adiciona um vértice sem nenhuma aresta associada a ele, pode parecer
        # igual em ambos os casos, mas não é.
        # Precisamos adicionar esse vértice no vetor de vértices e também alocar
        # seu espaço para as arestas.

        # Define nome da vértice
        self.labels[label] = self.vertices
        self.vertices += 1

        self.lista.append(list())

    def removerVertice(self, label):
        # Remove um vértice do grafo, elimina a linha e coluna dele da matriz
        # e a referência dele da lista, junto com todas as arestas que chegam
        # e saem dele.
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

        listaTmp = list()
        for vertice in range(self.vertices + 1):
            if vertice == idVertice:
                continue
            listaTmp.append(self.lista[vertice])

        self.lista = listaTmp

    def labelVertice(self, indice):
        # Funções básicas para retornar o nome de um vértice.
        label = [k for k, v in self.labels.items() if v == indice]
        return (label[0])

    def imprimeGrafo(self, cor=True):
        # Imprimir o grafo no console, tentem deixar próximo da representação
        # dos slides (não precisa da grade da matriz).
        if cor and self.cores > 0:
            print("Cores:", self.cores)
            for valor in range(self.vertices):
                print(valor, " C-", self.consultaCor(valor), sep="",  end=" ")
                print(":", self.lista[valor])
        else:
            for valor in range(self.vertices):
                print(valor, ":", self.lista[valor])

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

        self.lista[origem].append((destino, peso))

        if self.direcionado and origem != destino:
            self.lista[destino].append((origem, peso))

        self._ordernarArestasDoVertice

        self.arestas += 1

    def removerAresta(self, origem, destino):
        # Remove uma aresta entre dois vértices no grafo, lembrando que no grafo
        # não direcionado deve ser removida a aresta de retorno também;
        # try:
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)

        for idx, aresta in enumerate(self.lista[origem]):
            if destino in aresta:
                self.lista[origem].pop(idx)

        # self.lista[origem].remove(self.lista[origem][destino])

        # No direcionado, remove o do destino, a origem
        if self.direcionado:
            for idx, aresta in enumerate(self.lista[destino]):
                if origem in aresta:
                    self.lista[destino].pop(idx)
            # self.lista[destino].remove(self.lista[origem][destino])

        self._ordernarArestasDoVertice

        self.arestas -= 1

    # except:
    #   print('Aresta inválida.')

    def existeAresta(self, origem, destino):
        # Verifica a existência de uma aresta, aqui vemos uma diferença
        # grande entre matriz e lista.
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)

        # Verifica se existe o destino na lista, ignorando o peso
        for aresta in self.lista[origem]:
            if destino in aresta:
                return True

        return False

    def pesoAresta(self, origem, destino):
        # Retorne o peso de uma aresta, aqui vemos uma diferença grande
        # entre matriz e lista.
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)
        # print('\nPESOARESTA CHAMADO', end=' ')
        # print('origem:', origem, end=' ')
        # print('destino:', destino)

        # print('self.lista[origem]', self.lista[origem])
        # print('self.lista[origem][destino]', self.lista[origem][destino])
        # print('self.lista[origem][destino][1]', self.lista[origem][destino][1])
        return self.lista[origem][destino][1]

    def pesoArestaLabel(self, origem, destino):
        # Retorne o peso de uma aresta, aqui vemos uma diferença grande
        # entre matriz e lista.
        # Converte os labels para indices
        if isinstance(origem, str):
            origem = self.labels.get(origem)
        if isinstance(destino, str):
            destino = self.labels.get(destino)
        # print('\nPESOARESTA CHAMADO', end=' ')
        # print('origem:', origem, end=' ')
        # print('destino:', destino)

        # print('self.lista[origem]', self.lista[origem])
        # print('self.lista[origem][destino]', self.lista[origem][destino])
        # print('self.lista[origem][destino][1]', self.lista[origem][destino][1])
        # Verifica se existe o destino na lista, ignorando o peso
        for aresta in self.lista[origem]:
            # print('aresta:', aresta)
            # print('aresta:', aresta)
            # print('aresta[0]:', aresta[0])
            # print('destino:', aresta[0])
            if destino == aresta[0]:
                return aresta[1]
        return None

    def retornarVizinhos(self, vertice):
        # Converte para numero
        if isinstance(vertice, str):
            vertice = self.labels.get(vertice)
        # Função para retorno dos vizinhos de um vértice, necessária pois não
        # teremos acesso a estrutura das arestas para os próximos algoritmos.
        vizinhos = list()

        # Retorna cada tupla com os vizinhos
        for aresta in self.lista[vertice]:
            tuplaTemp = (self.labelVertice(aresta[0]), aresta[0])
            vizinhos.append(tuplaTemp)

        return vizinhos

    def temCicloTres(self):
        # Validar estrutura de dados dos vizinhos
        for verticeAtual in range(self.vertices):
            vizinhos = self.retornarVizinhos(verticeAtual)
            for vizinho in vizinhos:
                subVizinhos = self.retornarVizinhos(vizinho[1])
                for subVizinho in subVizinhos:
                    if subVizinho in vizinhos:
                        return True
        return False

    def planaridade(self):
        if self.vertices <= 2:  #
            return True  # O Grafo é planar
        elif self.temCicloTres():  # Verificar se contém ciclo três
            # Validar funcionamento do código das arestas (adicionar/remover)
            if (self.arestas <= (3 * self.vertices) - 6):  # A ≤ 3V – 6
                return True  # Pode ser planar

        return False

    def grauVertice(self, vertice):
        # Converte os labels para indices
        if isinstance(vertice, str):
            vertice = self.labels.get(vertice)
        if isinstance(vertice, list):  # Se já for uma lista, retorna o len dela
            return len(vertice)

        # print(vertice)
        # print(type(vertice))

        return len(self.lista[vertice])

    def labelsOrdenadosPorGrau(self):
        return sorted(self.labels, reverse=True, key=self.grauVertice)

    def insereCor(self, label, cor):
        # Converte os indices para labels
        if isinstance(label, int):
            label = list(self.labels.keys())[list(self.labels.values()).index(label)]

        # Define nome da vértice, para a cor
        self.dictCores[label] = cor

    def consultaCor(self, vertice):
        # Converte os indices para labels
        if isinstance(vertice, int):
            vertice = list(self.labels.keys())[list(self.labels.values()).index(vertice)]
        return self.dictCores.get(vertice)

    def welsh(self):
        inicio = time.time()

        # etapa 1: ordenar as vertices do grafo conforme o seu grau, em ordem decrescente
        grafo_ordenado = self.labelsOrdenadosPorGrau()

        # etapa 2: para cada cor X na lista de cores
        # define primeira cor
        self.cores += 1  # Primeira cor: 1 / Cor Inicial
        self.listaCores.append(self.cores)  # Lista de cores: [1]

        # para cada cor X na lista de cores
        for cor_atual in self.listaCores:
            # i) navega pela lista de vertices ordenadas, e se o vertice não foi colorido ainda,
            # e não é adjacente a uma vértice com a cor X atribuída, designa ela a ele mesmo, caso contrário move a
            # próxima vértice.

            remover = list()
            # Navega pela lista de vertices ordenada conforme o grau:
            for label_vertice_atual in grafo_ordenado:
                # Se a vértice já foi colorida, remove ela da fila e pula para a próxima
                # if self.consultaCor(label_vertice_atual) is not None:
                #     grafo_ordenado.remove(label_vertice_atual)
                #     continue
                # obtém cores dos vizinhos (vértices adjacentes)
                vizinhos = self.retornarVizinhos(label_vertice_atual)  # retorna os labels dos vizinhos e seus indices
                cor_vizinhos = list()  # lista de cores atribuídas aos vizinhos
                for vizinho in vizinhos:
                    cor_vizinhos.append(self.consultaCor(vizinho[0]))  # consulta cor do vizinho, com base no label
                # Verifica se é adjacente a uma vértice com a cor X atribuída
                if cor_atual not in cor_vizinhos:
                    self.insereCor(label_vertice_atual, cor_atual)
                    remover.append(label_vertice_atual)  # Remove da lista atual, após inserir
                    # grafo_ordenado.remove(label_vertice_atual) # Remove da lista atual, após inserir

            # Limpeza dos vertices para evitar bugs
            if remover:
                grafo_ordenado = list(filter(lambda x: x not in remover, grafo_ordenado))

            # Validar se colorimos todas as vértices:
            if not grafo_ordenado:  # listas vazias são falsas em python
                break

            # ii) após a última vértice, move para  a próxima cor e começa novamente
            self.cores += 1  # Próxima cor: 2 / Cor Inicial
            self.listaCores.append(self.cores)  # Lista de cores: [1, 2]

            # if self.cores < 2:
            #     break

        fim = time.time()
        tempo_decorrido = fim - inicio
        print("Tempo decorrido:", tempo_decorrido, "segundos")
        print("Cores:", self.cores)

    def welshDebug(self):
        inicio = time.time()

        # etapa 1: ordenar as vertices do grafo conforme o seu grau, em ordem decrescente
        grafo_ordenado = self.labelsOrdenadosPorGrau()
        print(grafo_ordenado)
        # for i in grafo_ordenado:
        #     print(self.lista[self.labels.get(i)])

        # etapa 2: para cada cor X na lista de cores
        # define primeira cor
        self.cores += 1  # Primeira cor: 1 / Cor Inicial
        self.listaCores.append(self.cores)  # Lista de cores: [1]

        # para cada cor X na lista de cores
        for cor_atual in self.listaCores:
            # i) navega pela lista de vertices ordenadas, e se o vertice não foi colorido ainda,
            # e não é adjacente a uma vértice com a cor X atribuída, designa ela a ele mesmo, caso contrário move a
            # próxima vértice.

            remover = list()
            # Navega pela lista de vertices ordenada conforme o grau:
            for label_vertice_atual in grafo_ordenado:
                print('Início')
                print('Grafo ordenado atual:', grafo_ordenado)
                print('Label atual:', label_vertice_atual)
                print('Consulta cor vertice atual', label_vertice_atual, 'cor:', self.consultaCor(label_vertice_atual))
                # Se o vértice já foi colorida, remove ela da fila e pula para a próxima
                # if self.consultaCor(label_vertice_atual) is not None:
                #     # grafo_ordenado.remove(label_vertice_atual)
                #     print('Novo grafo ordenado:', grafo_ordenado)
                #     print('Cor já preenchida, pular', '--------------------', sep='\n')
                #     continue
                # obtém cores dos vizinhos (vértices adjacentes)
                vizinhos = self.retornarVizinhos(label_vertice_atual)  # retorna os labels dos vizinhos e seus indices
                cor_vizinhos = list()  # lista de cores atribuídas aos vizinhos
                print('Vizinhos:', vizinhos)
                for vizinho in vizinhos:
                    print('Cor vizinho', vizinho[0], 'é', self.consultaCor(vizinho[0]))
                    cor_vizinhos.append(self.consultaCor(vizinho[0]))  # consulta cor do vizinho, com base no label
                print('Cores dos vizinhos são:', cor_vizinhos)
                print('Cor atual do loop:', cor_atual)
                # Verifica se é adjacente a um vértice com a cor X atribuída
                if cor_atual not in cor_vizinhos:
                    print('Cor atual não está em cor_vizinhos')
                    self.insereCor(label_vertice_atual, cor_atual)
                    remover.append(label_vertice_atual)  # Remove da lista atual, após inserir
                    # grafo_ordenado.remove(label_vertice_atual) # Remove da lista atual, após inserir
                    print('Cor da vértice atual', label_vertice_atual, 'cor:',self.consultaCor(label_vertice_atual))

                print('--------------------')

            # Limpeza dos vertices para evitar bugs
            if remover:
                grafo_ordenado = list(filter(lambda x: x not in remover, grafo_ordenado))

            # Validar se colorimos todas as vértices:
            # print('Grafo ordenado atual:', grafo_ordenado)
            if not grafo_ordenado:  # listas vazias são falsas em python
                print('Lista vazia !!!')
                break

            # ii) após a última vértice, move para  a próxima cor e começa novamente
            self.cores += 1  # Próxima cor: 2 / Cor Inicial
            self.listaCores.append(self.cores)  # Lista de cores: [1, 2]

            # if self.cores < 2:
            #     break

        fim = time.time()
        tempo_decorrido = fim - inicio
        print("Tempo decorrido:", tempo_decorrido, "segundos")
        print("Cores:", self.cores)

    def consultaSaturacao(self, vertice):
        # Converte os indices para labels
        if isinstance(vertice, int):
            vertice = list(self.labels.keys())[list(self.labels.values()).index(vertice)]

        vizinhos = self.retornarVizinhos(vertice)  # retorna os labels dos vizinhos e seus indices
        cor_vizinhos = set()  # lista de cores atribuídas aos vizinhos
        for vizinho in vizinhos:
            corVizinho = self.consultaCor(vizinho[0])
            if corVizinho is not None:
                cor_vizinhos.add(corVizinho)  # consulta cor do vizinho, com base no label

        return len(cor_vizinhos)

    def ordenaPorSaturacao(self, subGrafo):
        return sorted(subGrafo, reverse=True, key=self.consultaSaturacao)

    def dsatur(self):
        inicio = time.time()

        # etapa 1: ordenar as vertices do grafo conforme o seu grau, em ordem decrescente
        grafo_ordenado = self.labelsOrdenadosPorGrau()

        # etapa 2: para cada cor X na lista de cores
        # define primeira cor
        self.cores += 1  # Primeira cor: 1 / Cor Inicial
        self.listaCores.append(self.cores)  # Lista de cores: [1]

        # Colorir o vértice com maior grau com a primeira cor
        self.insereCor(grafo_ordenado[0], self.cores)
        grafo_ordenado.remove(grafo_ordenado[0])

        while grafo_ordenado:
            # ordena por saturação e seleciona o com maior saturação e grau
            label_vertice_max = self.ordenaPorSaturacao(grafo_ordenado)[0]

            # obtém cores dos vizinhos (vértices adjacentes)
            vizinhos = self.retornarVizinhos(label_vertice_max)  # retorna os labels dos vizinhos e seus indices
            cor_vizinhos = set()  # lista de cores atribuídas aos vizinhos
            for vizinho in vizinhos:
                corVizinho = self.consultaCor(vizinho[0])
                if corVizinho is not None:
                    cor_vizinhos.add(corVizinho)  # consulta cor do vizinho, com base no label

            coresDisponiveis = set(self.listaCores) - cor_vizinhos

            if coresDisponiveis:  # Sets e listas vazios são falsos
                self.insereCor(label_vertice_max, min(coresDisponiveis))  # Insere a primeira cor disponível
                grafo_ordenado.remove(label_vertice_max)  # Remove o vértice da fila, pois está colorido
            else:
                # caso não possua mais cores disponíveis, cria uma nova
                self.cores += 1  # Próxima cor: 2 / Cor Inicial
                self.listaCores.append(self.cores)  # Lista de cores: [1, 2]
                self.insereCor(label_vertice_max, self.cores)  # Insere a primeira cor disponível
                grafo_ordenado.remove(label_vertice_max)  # Remove o vértice da fila, pois está colorido

        fim = time.time()
        tempo_decorrido = fim - inicio
        print("Tempo decorrido:", tempo_decorrido, "segundos")
        print("Cores:", self.cores)


    def dsaturDebug(self):
        inicio = time.time()

        # etapa 1: ordenar as vertices do grafo conforme o seu grau, em ordem decrescente
        grafo_ordenado = self.labelsOrdenadosPorGrau()
        print(grafo_ordenado)
        # for i in grafo_ordenado:
        #     print(self.lista[self.labels.get(i)])

        # etapa 2: para cada cor X na lista de cores
        # define primeira cor
        self.cores += 1  # Primeira cor: 1 / Cor Inicial
        self.listaCores.append(self.cores)  # Lista de cores: [1]

        # Colorir o vértice com maior grau com a primeira cor
        self.insereCor(grafo_ordenado[0], self.cores)
        grafo_ordenado.remove(grafo_ordenado[0])

        while grafo_ordenado:
            print('Início')
            print('Grafo ordenado atual:', grafo_ordenado)
            # ordena por saturação e seleciona o com maior saturação e grau
            label_vertice_max = self.ordenaPorSaturacao(grafo_ordenado)[0]

            for ver in self.ordenaPorSaturacao(grafo_ordenado):
                print('Saturação do vértice[', ver, ']: ', self.consultaSaturacao(ver), sep='')

            print('Subgrafo ordenado atual:', grafo_ordenado)
            print('Label atual:', label_vertice_max)

            # obtém cores dos vizinhos (vértices adjacentes)
            vizinhos = self.retornarVizinhos(label_vertice_max)  # retorna os labels dos vizinhos e seus indices
            cor_vizinhos = set()  # lista de cores atribuídas aos vizinhos
            print('Vizinhos:', vizinhos)
            for vizinho in vizinhos:
                corVizinho = self.consultaCor(vizinho[0])
                print('Cor vizinho', vizinho[0], 'é', corVizinho)
                if corVizinho is not None:
                    cor_vizinhos.add(corVizinho)  # consulta cor do vizinho, com base no label
            print('Cores dos vizinhos são:', cor_vizinhos)

            coresDisponiveis = set(self.listaCores) - cor_vizinhos
            print('Cores disponíveis são:', coresDisponiveis)

            if coresDisponiveis:  # Sets e listas vazios são falsos
                print('Cor inserida:', min(coresDisponiveis))
                self.insereCor(label_vertice_max, min(coresDisponiveis))  # Insere a primeira cor disponível
                grafo_ordenado.remove(label_vertice_max)  # Remove o vértice da fila, pois está colorido
            else:
                # caso não possua mais cores disponíveis, cria uma nova
                self.cores += 1  # Próxima cor: 2 / Cor Inicial
                self.listaCores.append(self.cores)  # Lista de cores: [1, 2]
                print('Cor inserida:', self.cores)
                self.insereCor(label_vertice_max, self.cores)  # Insere a primeira cor disponível
                grafo_ordenado.remove(label_vertice_max)  # Remove o vértice da fila, pois está colorido

            print('-------------------')

        fim = time.time()
        tempo_decorrido = fim - inicio
        print("Tempo decorrido:", tempo_decorrido, "segundos")
        print("Cores:", self.cores)
