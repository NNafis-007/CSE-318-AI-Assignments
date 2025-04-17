import heapq
import itertools
from N_Puzzle import N_Puzzle

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = itertools.count()  #to distinguish if priority same

    def push(self, priority : int, item : 'N_Puzzle'):
        count = next(self.counter)
        # Add a tuple: (priority, count, item)
        heapq.heappush(self.heap, (priority, count, item))

    def pop(self) -> tuple[int, 'N_Puzzle']:
        if self.heap:
            priority, count, item = heapq.heappop(self.heap)
            return priority, item
        else:
            raise IndexError("pop from an empty priority queue")
    
    def size(self):
        return len(self.heap)

        