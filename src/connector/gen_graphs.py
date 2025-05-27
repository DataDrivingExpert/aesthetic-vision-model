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
            'postures_right_4', # 11
            'abstract_left_1', # 12
            'abstract_left_2', # 13
            'abstract_left_3', # 14
            'abstract_left_4',  # 15
            'abstract_middle_1',  # 16
            'abstract_middle_2',  # 17
            'abstract_middle_3',  # 18
            'abstract_middle_4',  # 19
            'abstract_right_1',   # 20
            'abstract_right_2',   # 21
            'abstract_right_3',   # 22
            'abstract_right_4',   # 23
            ]
        self.symmetry_graph = None
        self.continuity_graph = None


    def __generate_vertices(self) -> list[Vertice]:
        vertices = []
        
        for i, cLabel in enumerate(self.CLASSES):
            vertices.append(Vertice(i, cLabel))
        return vertices

    def generate_graph_symmetry(self) -> GraphSymmetry:
        v = self.__generate_vertices()
        g = GraphSymmetry(len(v), v)
        # Postures
        g.add_edge(v[0], v[8])
        g.add_edge(v[1], v[9])
        g.add_edge(v[2], v[10])
        g.add_edge(v[3], v[11])

        # Abstract
        g.add_edge(v[12], v[20])
        g.add_edge(v[13], v[21])
        g.add_edge(v[14], v[22])
        g.add_edge(v[15], v[23])
        g.add_edge(v[15], v[23])

        return g

    def generate_graph_continuity(self) -> GraphContinuity:
        v = self.__generate_vertices()
        g = GraphContinuity(len(v), v)

        # Postures
        g.add_edge(v[0], v[1])
        g.add_edge(v[0], v[4])
        g.add_edge(v[1], v[2])
        g.add_edge(v[1], v[5])
        g.add_edge(v[2], v[3])
        g.add_edge(v[2], v[6])
        g.add_edge(v[3], v[7])
        g.add_edge(v[4], v[5])
        g.add_edge(v[4], v[8])
        g.add_edge(v[5], v[6])
        g.add_edge(v[5], v[9])
        g.add_edge(v[6], v[7])
        g.add_edge(v[6], v[10])
        g.add_edge(v[7], v[11])
        g.add_edge(v[8], v[9])
        g.add_edge(v[9], v[10])
        g.add_edge(v[10], v[11])

        # Abstract
        g.add_edge(v[12], v[13])
        g.add_edge(v[12], v[16])
        g.add_edge(v[13], v[14])
        g.add_edge(v[13], v[17])
        g.add_edge(v[14], v[15])
        g.add_edge(v[14], v[18])
        g.add_edge(v[15], v[19])
        g.add_edge(v[16], v[17])
        g.add_edge(v[16], v[20])
        g.add_edge(v[17], v[18])
        g.add_edge(v[17], v[21])
        g.add_edge(v[18], v[19])
        g.add_edge(v[18], v[22])
        g.add_edge(v[19], v[23])
        g.add_edge(v[20], v[21])
        g.add_edge(v[21], v[22])
        g.add_edge(v[22], v[23])

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

    
    
