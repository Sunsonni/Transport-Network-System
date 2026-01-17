# Using Hash Table
class Graph:
    def __init__(self):
        # Adjacency list: {city: {neighbor_city: weight}}
        self.adj = {}

    def add_node(self, city):
        # Adds city to the graph if it doesn't exist yet
        if city not in self.adj:
            self.adj[city] = {}
        
    def add_edge(self, src, dst, weight):
        # Adds directed road from src to dst with gvn weight
        # Automatically adds cities if not previosly defined
        self.add_node(src)
        self.add_node(dst)
        self.adj[src][dst] = weight

    def remove_edge(self, src, dst):
        # Removes directed road from src to dst
        if src in self.adj and dst in self.adj[src]:
            del self.adj[src][dst]

    def remove_node(self, city):
        # Removes city and all of its connecting roads
        if city in self.adj:
            del self.adj[city]
        
        for src in self.adj:
            if city in self.adj[src]:
                del self.adj[src][city]
    
    def to_adjacency_list(self):
        # Returns string of graph as adjacnecy list
        lines = []

        for src in self.adj:
            edges = []
            for dst, weight in self.adj[src].items():
                edges.append(f"{dst}({weight})")

            if edges:
                lines.append(f"{src}: {', '.join(edges)}")
            else:
                lines.append(f"{src}:")
                
        return "\n".join(lines)