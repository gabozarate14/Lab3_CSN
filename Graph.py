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
            if vertex2 not in self.adjacency_list[vertex1]:
                self.adjacency_list[vertex1].append(vertex2)

        if vertex2 in self.adjacency_list:
            if vertex1 not in self.adjacency_list[vertex2]:
                self.adjacency_list[vertex2].append(vertex1)

    def __str__(self):
        result = ""
        for vertex, neighbors in self.adjacency_list.items():
            result += f"{vertex}: {', '.join(neighbors)}\n"
        return result

    def get_number_of_vertices(self):
        return len(self.adjacency_list)

    def get_number_of_edges(self):
        total_edges = 0
        for vertex in self.adjacency_list:
            total_edges += len(self.adjacency_list[vertex])
        return total_edges // 2

    def bfs_distances(self, start_vertex):
        visited = {vertex: False for vertex in self.adjacency_list}

        distances = {vertex: float("inf") for vertex in self.adjacency_list}
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

    def calculate_mean_closeness(graph):
        n = graph.get_number_of_vertices()
        c = 0
        for vertex in graph.adjacency_list:
            distances = graph.bfs_distances(vertex)
            ci = 0
            for dij in distances.values():
                if dij != 0:
                    ci += (1/dij)
            c += ci / (n-1)

        return c/n