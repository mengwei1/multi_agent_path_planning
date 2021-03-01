"""

Dijkstra search

author: Wei Meng

"""
from PriorityQueue import PriorityQueue
from tqdm import tqdm


class Dijkstra():
    def __init__(self, graph):
        self.graph = graph
        self.paths = dict()
        '''
        {
            'a': {
                'b': {
                    'cost': 50,
                    'path': ['a','d','c','b']
                },
                'c':{
                    'cost': 100,
                    'path': ['a','d','c']
                }
            }
        }
        '''

    def traverse(self):
        for point_1 in tqdm(self.graph.points):
            self.paths[point_1] = dict()
            for point_2 in self.graph.points:
                if point_1 == point_2:
                    continue
                # print('search route for %s to %s' % (point_1, point_2))
                self.search(point_1, point_2)
                # print('route found, path is %s' % self.paths[point_1][point_2]['path'])

    def search(self, start, end):
        frontier = PriorityQueue()
        frontier.put(0, start)

        cost_so_far = dict()
        cost_so_far[start] = 0

        came_from = dict()
        came_from[start] = None

        while not frontier.is_empty():
            pri, current = frontier.get()

            if current == end:
                self.paths[start].update(self.reconstruct_path(end, came_from))
                break

            neighbors = [neighbor.end for neighbor in self.graph.neighbors(current)]
            for neighbor in neighbors:
                new_cost = cost_so_far[current] + self.graph.cost(current, neighbor)
                if neighbor not in cost_so_far.keys() or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    frontier.put(new_cost, neighbor)

    def reconstruct_path(self, end, came_from):
        result = dict()
        result[end] = dict()
        path = list()
        cost = 0

        current = end

        while came_from[current]:
            cost += self.graph.cost(came_from[current], current)
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()

        result[end]['cost'] = cost
        result[end]['path'] = path
        return result