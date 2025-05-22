import numpy as np


class Vertice(object):
    def __init__(self, id:int, cLabel:str='Non Label'):
        self.id = id
        self.cLabel = cLabel
    
    def __str__(self):
        return f"Vertice(id={self.id}, class_label={self.cLabel})"
    
    def get_id(self) -> int:
        return self.id

class Graph(object):
    def __init__(self, size:int, vertices:list[Vertice]):
        self.size = size
        self.V = vertices
        self.graph = np.zeros((size, size), dtype=int)

    def add_edge(self, u:Vertice, v:Vertice, w:int=1):
        self.graph[u.get_id()][v.get_id()] = w
        self.graph[v.get_id()][u.get_id()] = w

    def is_connected(self, u:Vertice, v:Vertice) -> bool:
        return self.graph[u.get_id()][v.get_id()] != 0
    
    def get_graph(self) -> np.ndarray:
        return self.graph
    
    def get_v_by_id(self, id:int) -> Vertice:
        for v in self.V:
            if v.get_id() == id:
                return v
        return None
    

class GraphSymmetry(Graph):
    def __init__(self,size:int,vertices:list[Vertice]):
        super().__init__(size,vertices)


class GraphContinuity(Graph):
    def __init__(self,size:int,vertices:list[Vertice]):
        super().__init__(size,vertices)