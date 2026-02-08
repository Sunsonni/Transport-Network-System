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
<<<<<<< HEAD
            smallest = i
=======
            smallest = i 
>>>>>>> b9aa1b58e8616f7a34cd63d46d67ee9f4b1ed60a
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

# Dijkstra shortest path
# Finds the shortest path from start city to end city
def dijkstra(graph, start, end, traffic_map):
    # Distance starts at 0
    heap = MinHeap()
    heap.insert(0, start) 

    # Stores shortest distance to each city and previous city
    distances = {start: 0}
    previous = {start: None}

    # Finds closest city
    while not heap.is_empty():
        current_dist, current_city = heap.extract_min()

        # Stop if destination is reached
        if current_city == end:
            break

        # Check all neighbors of current city
        for neighbor, base_weight in get_neighbors(graph, current_city):
            cost = base_weight + traffic_map.get(current_city, neighbor)
            new_dist = current_dist + cost

            # Make sure a shorter path doesn't exist
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_city
                heap.insert(new_dist, neighbor)

    # If destination wasn't reached
    if end not in distances:
        return None, None

    # Rebuild shortest path
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = previous[cur]
    path.reverse()

    return path, distances[end]

# K shortest path query using Dijkstra
def k_shortest_paths(graph, start, end, k, traffic_map):
    """Find K shortest pasths from start to end"""
    paths = []

    # Find the first shortest path
    path, cost = dijkstra(graph, start, end, traffic_map)
    if path:
        paths.append((path, cost))

        # Finding another paths by blocking fromer paths
        while len(paths) < k:
            # Add a traffic delta to the last found path to block it
            modified_traffic = TrafficMap(traffic_map.size)

            # Copy exisiting traffic
            for j in range(traffic_map.size):
                if traffic_map.table[j]:
                    (src, dst), delta = traffic_map.table[j]
                    modified_traffic.update(src, dst, delta)

            # Block edges in all previous baths
            for prev_path, _ in paths:
                for i in range(len(prev_path) - 1):
                    modified_traffic.update(prev_path[i], prev_path[i+1], 999999) # A large delta number to block paths

            # Finding a new path
            new_path, new_cost = dijkstra(graph, start, end, modified_traffic)
            
            if not new_path or new_cost >= 999999:
                break
            paths.append((new_path, new_cost))

        return paths
    

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 graph_query1.py input1.txt commands2.txt")
        sys.exit(1)

    graph_file, commands_file = sys.argv[1], sys.argv[2]

    graph = Graph()
    try:
        with open(graph_file, "r") as f:
           # False = citites, True = roads
            mode = False 
            for line in f:
                line = line.strip()
                if line == "CITIES": #if line is CITITES, switch to city mode and skip line
                    continue
                if line == "ROADS":
                    mode = True
                    continue
                if not line: # if line is empty skip it
                    continue

                if mode:
                    parts = line.split()
                    if len(parts) >= 3:
                        graph.add_edge(parts[0], parts[1], int(parts[2]))
                    else:
                        graph.add_node(line)
            
            # Initialize traffic map
            traffic_map = TrafficMap()
    except:  
        print("Aww man")

    # Process command file
    with open(commands_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            # Handle traffic updates
            if parts[0] == "TRAFFIC_REPORT":
                traffic_map.update(parts[1], parts[2], int(parts[3]))

            # Handle shortest path query
            elif parts[0] == "QUERY" and parts[1] == "SHORTEST_PATH":
                path, cost = dijkstra(graph, parts[2], parts[3], traffic_map)
                if path:
                    print(
                        f"SHORTEST_PATH {parts[2]} {parts[3]}: "
                        f"{' -> '.join(path)} (cost: {cost})"
                    )

            # Handle k paths query
            elif parts[0] == "QUERY" and parts[1] == "K_PATHS":
                paths = k_shortest_paths(
                    graph,
                    parts[2],
                    parts[3],
                    int(parts[4]),
                    traffic_map
                )
                print(f"K_PATHS {parts[2]} {parts[3]}:")
                for i, (p, c) in enumerate(paths):
                    print(f"{i+1}) {' -> '.join(p)} ({c})")

if __name__ == "__main__":
    main()
               