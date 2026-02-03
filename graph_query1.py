"""Module 2: Traffic and Priority Query System
This module 2 extends to the graph to module"""

from graph import Graph
import sys

# Min-Heap implementation for the Dijkstra's algorithm
class MinHeap:
    "The Min-heap implementation for priority queue in Dijkstra's algorithm,"
    "stores tuples of (distance, city) and where distance is the priority."

    def __init__(self):
        self.heap = [] # Initialized an empty min-heap
        self.size = 0