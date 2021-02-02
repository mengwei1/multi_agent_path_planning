class LucadGraph:
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges

    def neighbors(self, point):
        return self.edges[str(point)]
