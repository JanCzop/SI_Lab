import heapq

class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        return heapq.heappop(self._heap)[1]

    def is_empty(self):
        return not bool(self._heap)

    def __len__(self):
        return len(self._heap)
