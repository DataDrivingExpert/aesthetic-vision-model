from src.classes.graph import GraphSymmetry, GraphContinuity, Vertice

class AestheticGraph(object):

    def __init__(self):
        self.CLASSES = [
            'postures_left_1',  # 0
            'postures_left_2',  # 1
            'postures_left_3',  # 2
            'postures_left_4',  # 3
            'postures_middle_1', # 4
            'postures_middle_2', # 5
            'postures_middle_3', # 6
            'postures_middle_4', # 7
            'postures_right_1', # 8
            'postures_right_2', # 9
            'postures_right_3', # 10
            'postures_right_4' # 11
            ]
        self.symmetry_graph = None
        self.continuity_graph = None


    def __generate_vertices(self) -> list[Vertice]:
        vertices = []
        for i, cLabel in enumerate(self.CLASSES):
            vertices.append(Vertice(i, cLabel))
        return vertices

    def generate_graph_symmetry(self) -> GraphSymmetry:
        vertices = self.__generate_vertices()
        g = GraphSymmetry(len(vertices), vertices)
        g.add_edge(vertices[0], vertices[8])
        g.add_edge(vertices[1], vertices[9])
        g.add_edge(vertices[2], vertices[10])
        g.add_edge(vertices[3], vertices[11])
        return g

    def generate_graph_continuity(self) -> GraphContinuity:
        vertices = self.__generate_vertices()
        g = GraphContinuity(len(vertices), vertices)

        v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11 = vertices
        g.add_edge(v0, v1)
        g.add_edge(v0, v4)
        g.add_edge(v1, v2)
        g.add_edge(v1, v5)
        g.add_edge(v2, v3)
        g.add_edge(v2, v6)
        g.add_edge(v3, v7)
        g.add_edge(v4, v5)
        g.add_edge(v4, v8)
        g.add_edge(v5, v6)
        g.add_edge(v5, v9)
        g.add_edge(v6, v7)
        g.add_edge(v6, v10)
        g.add_edge(v7, v11)
        g.add_edge(v8, v9)
        g.add_edge(v9, v10)
        g.add_edge(v10, v11)
        return g

    @property
    def graphs(self) -> tuple[GraphSymmetry, GraphContinuity]:
        if self.symmetry_graph is None:
            self.symmetry_graph = self.generate_graph_symmetry()

        if self.continuity_graph is None:
            self.continuity_graph = self.generate_graph_continuity()

        return self.symmetry_graph, self.continuity_graph

if __name__ == '__main__':
    aesthetic_gp = AestheticGraph()
    symmetry_gp, continuity_gp = aesthetic_gp.graphs

    print("Graph of symmetry \n", symmetry_gp.get_graph(),'\n')
    print("Graph of continuity \n", continuity_gp.get_graph(), '\n')
