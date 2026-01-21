# Functions from Graph: 
#     add_node(self, city)
#     add_edge(self, src, dst, weight)
#     remove_node(self, city)
#     remove_edge(self, src, dst)
#     to_adjacency_list(self)

from graph import Graph

import sys

try:
    filename = sys.argv[1]

    graph = Graph()
    mode = False

    with open(filename, "r") as f:
        for line in f:
            clean_line = line.strip()
            if clean_line == "CITIES":
                continue
            if clean_line == "ROADS":
                mode = True
                continue
            
            if mode:
                src, dst, weight = clean_line.split(" ")
                graph.add_edge(src, dst, weight)
                continue
                
            graph.add_node(clean_line)
    output = graph.to_adjacency_list()
    print(output)
except Exception as e:
    print(f"Error: {e}")
    
    

