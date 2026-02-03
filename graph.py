# Using Hash Table
class Graph:
    def __init__(self):
        self.size = 100
        self.nodes = [None] * self.size # array for the City name
        self.weights = [None] * self.size # array for the city details

    def hash(self, key, i): # uses ASCII sum + linear probing
        h = 0
        
        for c in key:
            h += ord(c)
        j = (h+ i) % self.size
        return j

    def add_node(self, city):
        i = 0 # probe counter
        
        while i < self.size:
            j = self.hash(city, i)

            # Checking for open slot
            if self.nodes[j] is None:
                self.nodes[j] = city # store city name
                self.weights[j] = [] # initilaizes other array for the city details
                return j
            elif self.nodes[j] == city:
                return j # already defined
            else:
                i += 1

        raise Exception("Hash table overflow")

        
    def add_edge(self, src, dst, weight): # Adds directed edge from src to dst
        # src = source, dst = destination
        self.add_node(src)
        self.add_node(dst)
        
        # finding src index
        i = 0
        while i < self.size:
            j = self.hash(src,i)
            
            if self.nodes[j] == src:
                self.weights[j].append((dst,weight))
                return
            i += 1
        
        raise Exception(f"Source city {src} not found")

    def remove_edge(self, src, dst): # Removes directed road from src to dst
        i = 0
        while i < self.size:
            j = self.hash(src,i)

            if self.nodes[j] == src:
                tmp = [(c, w)
                    for (c, w) in self.weights[j] # c = neighboring city, w = its weight
                    if c != dst]
                self.weights[j] = tmp
                return
            i += 1

    def remove_node(self, city): # Removes city and all of its connecting roads
        i = 0
        while i < self.size:
            j = self.hash(city, i)

            if self.nodes[j] == city:
                self.nodes[j] = None
                self.weights[j] = None
                break
            i += 1
        
        # remove city from any remaining edges
        for n in range(self.size):
            if self.weights[n] is not None:
                tmp = [(c, w)
                       for (c, w) in self.weights[n]
                       if c != city]
                self.weights[n] = tmp
    
    def to_adjacency_list(self): # Returns string representation of graph as list
        lines = []
        
        for i in range(self.size):
            if self.nodes[i] is not None:
                edges = [f"{c}({w})"
                     for (c,w) in self.weights[i]]
                if edges:
                    lines.append(f"{self.nodes[i]}: {', '.join(edges)}")
                else:
                    lines.append(f"{self.nodes[i]}:")
        return "\n".join(lines)