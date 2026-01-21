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

    with open(filename, "r") as f:
        for line in f:
            if line.strip() in ("CITIES", "ROADS"):
                print(line.strip())
                continue
            
            
    output = graph.to_adjacency_list()
    print(output)
    # print(contents)
            
except Exception as e:
    print(f"Error: {e}")
    
    

