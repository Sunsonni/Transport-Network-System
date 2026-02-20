from graph import Graph
from graph_query1 import dijkstra, k_shortest_paths, TrafficMap
from datetime import datetime
from collections import deque

def time_converter(t):
    return datetime.strptime(t, "%H:%M")

class TransportSchedule:
    def __init__(self):
        self.graph = Graph()
        self.traffic_map = TrafficMap()
        self.queue = deque() # to structurely order deliverys
        self.undo_stack = [] # undos the last action
        self.history = [] # shows order of completed deliverys

    def schedule_delivery(self, src, dst, time): # schedules the deliveries
        delivery = (time, f"{src}->{dst} at {time}")
        self.queue.append(delivery)
        self.undo_stack.append(("shedule", delivery)) # this saves the action to undo

        return f"Scehduled: {delivery[1]}"
    
    def complete_delivery(self): # Completes next delivery from queue
        if not self.queue:
            return "No deliveries left"
        
        delivery = self.queue.popleft()
        self.history.append(delivery)
        self.history.sort(key=lambda x: time_converter(x[0]))
        self.undo_stack.append(("complete", delivery))
        return f"Completed: {delivery[1]}"
    
    def undo_last(self): # undos the previous item
        if not self.undo_stack:
            return "Nothing to undo"
        
        action, delivery = self.undo_stack.pop()
        if action == "schedule":
            if delivery in self.queue:
                self.queue.remove(delivery)
        elif action == "complete":
            if delivery in self.history:
                self.history.remove(delivery)
            self.queue.appendleft(delivery)

        return "Previous action undone"
    
    def record_history(self): # Tracks order of all completed delivery
        return self.complete_delivery()
    
    def query_history(self,start_time, end_time): # shows the list of completed deliveries in time span
        results = []
        for d in self.history:
            delivery_time = time_converter(d[0])
            if time_converter(start_time) <= delivery_time <= time_converter(end_time):
                results.append(d[1])

        if not results:
            return "No deliveries within the range"
        output = f"History between {start_time} and {end_time}:\n"
        output += "\n".join(results)
        
        return output
    
    def shortest_path(self, src, dst): # finds shortest path between cities
        if self.traffic_map:
            path, cost = dijkstra(self.graph, src, dst, self.traffic_map)
        else:
            path, cost = dijkstra(self.graph, src, dst, TrafficMap())
        
        if path:
            return f"Shortest path {src} -> {dst}: {' -> '.join(path)} (cost: {cost})"
        else:
            return f"No path found from {src} to {dst}"
        
    def k_shortest_paths(self, src, dst, k): # finds multiple short paths between cities
        if self.traffic_map:
            paths = k_shortest_paths(self.graph, src, dst, k, self.traffic_map)
        else:
            paths = k_shortest_paths(self.graph, src, dst, k, TrafficMap())
        
        if not paths:
            return f"No paths found from {src} to {dst}"
        
        output = f"K paths {src} -> {dst}:\n"
        for i, (p, c) in enumerate(paths):
            output += f"{i+1}) {' -> '.join(p)} ({c})\n"
        
        return output.strip()