import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = list()

    def get(self):
        return heapq.heappop(self.elements)

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, priority, item):
        heapq.heappush(self.elements, [priority, item])
