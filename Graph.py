from collections import deque

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 == vertex2:
            return
        if vertex1 in self.adjacency_list:
            self.adjacency_list[vertex1].append(vertex2)
        if vertex2 in self.adjacency_list:
            self.adjacency_list[vertex2].append(vertex1)

    def __str__(self):
        result = ""
        for vertex, neighbors in self.adjacency_list.items():
            result += f"{vertex}: {', '.join(neighbors)}\n"
        return result

    def bfs_distances(self, start_vertex):
        visited = {vertex: False for vertex in self.adjacency_list}
        distances = {vertex: float('inf') for vertex in self.adjacency_list}

        queue = deque()
        queue.append(start_vertex)
        visited[start_vertex] = True
        distances[start_vertex] = 0

        while queue:
            current_vertex = queue.popleft()
            for neighbor in self.adjacency_list[current_vertex]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    distances[neighbor] = distances[current_vertex] + 1

        return distances

    def closeness_centrality(graph):
        total_closeness = 0
        for vertex in graph.adjacency_list:
            distances = graph.bfs_distances(vertex)
            total_distance = sum(distances.values())
            if total_distance != 0:
                closeness = 1 / total_distance
                total_closeness += closeness

        return total_closeness / len(graph.adjacency_list)