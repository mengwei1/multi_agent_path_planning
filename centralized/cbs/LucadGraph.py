class LucadGraph:
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges
        self.average_edge_weight = self.get_average_edge_weight()

    def get_average_edge_weight(self):
        sum = 0
        cnt = 0
        for start in self.edges.keys():
            for edge in self.edges[start]:
                sum += int(edge.length)
                cnt += 1
        return sum / cnt

    def neighbors(self, point):
        return self.edges[str(point)]

    def cost(self, start, end):
        if start not in self.edges.keys():
            return float("inf")
        elif start == end:
            # TODO
            # 如果等待的cost为0,那么算法容易陷入无限等待
            # 所以应该给等待施加惩罚
            # 这个惩罚应该是多少呢?
            # 地图所有edge的cost的平均?
            return self.average_edge_weight
        else:
            for edge in self.edges[start]:
                if edge.end == end:
                    return int(edge.length)
            return float("inf")
