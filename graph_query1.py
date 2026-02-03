# Module 2: Traffic and Priority Query System
# This module 2 extends to the graph of module 1

from graph import Graph
import sys

# Min-Heap implementation for the Dijkstra's algorithm
class MinHeap:
   # The Min-heap implementation for priority queue in Dijkstra's algorithm, which
    # stores tuples of (distance, city) and where distance is the priority.

    def __init__(self):
        self.heap = [] # Initialized an empty min-heap
    
    def insert(self, distance, city):
        # maintain min-heap property while inserting new element
        self.heap.append((distance, city))
        self._bubble_up(len(self.heap) - 1)

    def extract_min(self):
        # Remove and return minium element
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return min_val
    
    def _bubble_up(self, i):
        # Maintain heap property by move element up
        while i > 0:
            parent = (i -1) // 2
            if self.heap[i][0] < self.heap[parent][0]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break
    
    def _bubble_down(self, i): 
        #move element down to maintain heap property
        while True:
            smallest - i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            
            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break
        
        def is_empty(self):
            return len(self.heap) == 0
    
# Traffic Map: Hash map for dynamic edge weights

class TrafficMap:
    def __init__(self, size=200):
        self.size = size
        self.table = [None] * size # Hash table to store edge weights

    def _hash(self, src, dst, i):
        # Hash function with linear probing
        h = sum(ord(c) for c in src) + sum(ord(c) for c in dst)
        return (h + i) % self.size
    
    def update(self, src, dst, delta): 
        # src = source city (where you start)
        # dst = destination city (where you end)
        # Delta means the CHANGE in weight (can be positive or negative), not the new weight itself
        # Update traffic delta for edge (src, dst)
        for i in range(self.size):
            j = self._hash(src, dst, i)
            if self.table[j] is None or self.table[j][0] == (src, dst):
                self.table[j] = ((src, dst), delta)
                return
            raise Exception("Traffic map overflow")
        
    def get(self, src, dst):
        # Get traffic delta for edge, returns 0 if none
        for i in range(self.size):
            j = self._hash(src, dst, i)
            if self.table [j] is None:
                return 0
            if self.table[j][0] == (src, dst):
                return self.table[j][1]
            return 0

# Helper function
# Helper function are resusable functions, handles repetitiveness and  prevents abstraction

def get_neighbors(graph, city): # Error checks
    # Gets all the neighbors of a city
    for i in range(graph.size):
        j = graph.hash(city, i)
        if graph.nodes[j] == city:
            return graph.weights[j] if graph.weights[j] else []
        return []
