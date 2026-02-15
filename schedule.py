from graph import Graph
from graph_query1 import dijkstra, k_shortest_paths

class TransportSchedule:
    def __init__(self, graph, traffic_map = None):
        self.graph = graph
        self.traffic_map = traffic_map
        self.queue = []         # FIFO queue
        self.undo_stack = []    # Undos the last made action
        self.history = []       # Sorts list of deliveries that have been completed

    def shedule_delivery(self, src, dst, time): # Scheduling the delivery
        delivery = (time, f"{src}->{dst} at {time}")
        self.queue.append(delivery)
        self.undo_stack.append(("schedule",delivery))
        
        return f"Scheduled: {delivery[1]}"
    
    def complete_delivery(self): # Completes delivery
        if not self.queue:
            return "No deliveries to complete"
        delivery = self.queue.pop(0)
        self.history.append(delivery) # Keeps the history sorted
        self.history.sort(key = lambda x: x[0]) # Sorts by time
        self.undo_stack.append(("complete", delivery))
        
        return f"Completed: {delivery[1]}"
    
    def undo_last(self): # Undos the last action
        if not self.undo_stack:
            return "Nothing to undo"
        action, delivery = self.undo_stack.pop()
        if action == "schedule":
            if delivery in self.queue:
                self.queue.remove(delivery)
            elif action == "complete":
                if delivery in self.history:
                    self.history.remove(delivery)
                self.queue.insert(0, delivery)
            return "Previous action undone"
    
    def record_history(self): # Records all deliveries to history (completed)
        return "Recorded history"
    
    def query_history(self, start_time, end_time): # history within a time range
        results = [d[1] for d in self.history if start_time <= d[0] <= end_time]
        if not results:
            return "No deliveries in the specified range"
        output = "History between {} and {}:\n- ".format(start_time, end_time)
        output += "\n-".join(results)

    def shortest_path(self, src, dst): # computes shortest path for delivery
        if self.traffic_map:
             path, cost = dijkstra(self.graph, src, dst, self.traffic_map)
        else: # Uses empty traffic map if there already isn't one
            from graph_query1 import TrafficMap
            path, cost = dijkstra(self.graph, src, dst, TrafficMap())
        if path:
            return f"Shortest path {src} -> {dst}: {' -> '.join(path)} (cost: {cost})"
        else:
             return f"No path found from {src} to {dst}"
        
    def k_shortest_paths(self, src, dst, k):
        if self.traffic_map:
            paths = k_shortest_paths(self.graph, src, dst, k, self.traffic_map)
        else:
            from graph_query1 import TrafficMap
            paths = k_shortest_paths(self.graph, src, dst, k, TrafficMap())
        if paths:
            output = f"K paths {src} -> {dst}:\n"
            for i, (p, c) in enumerate(paths):
                output += f"{i+1}) {' -> '.join(p)} ({c})\n"
            return output.strip()
        else:
            return f"No paths found from {src} to {dst}"