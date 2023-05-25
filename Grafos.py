class Grafos:
    def __init__(self, direcionado=False, ponderado=False):
        self.ponderado = ponderado
        self.direcionado = direcionado

        self.vertices = 0
        self.arestas = 0
