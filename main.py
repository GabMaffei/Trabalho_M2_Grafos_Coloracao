from GrafoLista import GrafoLista
import numpy as np

if __name__ == '__main__':
    pass
    # grafoUm = GrafoLista()
    # grafoUm.openFile('/content/drive/MyDrive/Colab Arquivos (CSV TXT)/Trabalho M1 - Grafos (Dijkstra)/espacoaereo.txt')
    # grafoUm.imprimeGrafo()
    # entrada = 5
    # dijkstra = grafoUm.dijkstra(entrada)
    # for vertice in range(len(dijkstra)):
    #     print("Distância do vertice", str(entrada), "para o vertice", str(vertice), "é", str(dijkstra[vertice]), sep=" ")
    # print(grafoUm.buscaDijkstra(0, 2))

    grafoDois = GrafoLista()
    grafoDois.openFile('Exemplos/k33.txt')
    # grafoDois.imprimeGrafo()
    grafoDois.dsatur()
    # grafoDois.imprimeGrafo(cor=True)
    # print(grafoDois.consultaSaturacao('4'))
    # for vertice in grafoDois.labelsOrdenadosPorGrau():
    #     print(grafoDois.consultaSaturacao(vertice))
    # print(grafoDois.labelsOrdenadosPorGrau())
    # print(grafoDois.ordenaPorSaturacao(grafoDois.labelsOrdenadosPorGrau()))

    # print(grafoDois.grauVertice(6))
    # print(grafoDois.consultaCor(6))
    # print(grafoDois.labelsOrdenadosPorGrau())
    # print(grafoDois.planaridade())
    ### print(grafoDois.welsh())
    # print(grafoDois.buscaProfunda(0, 4))
    # print(grafoDois.buscaLargura(0, 4))
    # print(grafoDois.retornarVizinhos(0))
