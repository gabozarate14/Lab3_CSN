from collections import deque
import random


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

    def get_vertices(self):
        return self.adjacency_list.keys()

    def copy(self):
        new_graph = Graph()

        for vertex in self.adjacency_list:
            new_graph.add_vertex(vertex)

        for vertex1, neighbors in self.adjacency_list.items():
            for vertex2 in neighbors:
                new_graph.add_edge(vertex1, vertex2)

        return new_graph

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
                    ci += (1 / dij)
            c += (ci / (n - 1))

        return c / n


    def calculate_mean_closeness_optimized(graph):
        n = graph.get_number_of_vertices()
        c = 0
        dd = {}
        for vertex in graph.adjacency_list:
            if len(graph.adjacency_list[vertex]) > 1:
                distances = graph.bfs_distances(vertex)
                dd[vertex] = distances
            else:
                continue

            ci = 0
            for dij in distances.values():
                if dij != 0:
                    ci += (1 / dij)
            c += (ci / (n - 1))

        for vertex in graph.adjacency_list:
            if len(graph.adjacency_list[vertex]) == 1:
                vertex2 = graph.adjacency_list[vertex][0]
                distances = dd.get(vertex2, {})
                distances = {key: value + 1 for key, value in distances.items()}

            else:
                continue

            ci = 0
            for dij in distances.values():
                if dij != 0:
                    ci += (1 / dij)
            c += (ci / (n - 1))

        return c / n

    def estimate_closeness_sum(graph, m_max, sort="original"):
        n = graph.get_number_of_vertices()
        c = 0
        m = 0
        adj_list = graph.adjacency_list.copy()

        if sort == "random":
            adj_list = sort_dict_randomly(adj_list)
        elif sort == "inc_degree":
            adj_list = sort_dict_by_list_length_ascending(adj_list)
        elif sort == "dec_degree":
            adj_list = sort_dict_by_list_length_descending(adj_list)

        for vertex in adj_list:
            if m == m_max:
                break
            distances = graph.bfs_distances(vertex)
            ci = 0
            for dij in distances.values():
                if dij != 0:
                    ci += (1 / dij)
            c += (ci / (n - 1))
            m += 1

        return c

    def estimate_closeness_sum_optimized(graph, m_max, sort="original"):
        n = graph.get_number_of_vertices()
        c = 0
        m = 0
        dd = {}
        adj_list = graph.adjacency_list

        if sort == "random":
            adj_list = sort_dict_randomly(adj_list)
        elif sort == "inc_degree":
            adj_list = sort_dict_by_list_length_ascending(adj_list)
        elif sort == "dec_degree":
            adj_list = sort_dict_by_list_length_descending(adj_list)

        for vertex in adj_list:
            if m == m_max:
                break
            if len(graph.adjacency_list[vertex]) > 1:
                distances = graph.bfs_distances(vertex)
                dd[vertex] = distances

            else:
                continue

            ci = 0
            for dij in distances.values():
                if dij != 0:
                    ci += (1 / dij)
            c += (ci / (n - 1))
            m += 1

        for vertex in adj_list:
            if m == m_max:
                break

            if len(graph.adjacency_list[vertex]) == 1:
                vertex2 = graph.adjacency_list[vertex][0]
                distances = dd.get(vertex2, {})
                distances = {key: value + 1 for key, value in distances.items()}

            else:
                continue
            ci = 0
            for dij in distances.values():
                if dij != 0:
                    ci += (1 / dij)
            c += (ci / (n - 1))
            m += 1

        return c


def sort_dict_randomly(input_dict):
    random_items = list(input_dict.items())
    random.shuffle(random_items)
    return dict(random_items)


def sort_dict_by_list_length_ascending(input_dict):
    return dict(sorted(input_dict.items(), key=lambda item: len(item[1])))


def sort_dict_by_list_length_descending(input_dict):
    return dict(sorted(input_dict.items(), key=lambda item: len(item[1]), reverse=True))