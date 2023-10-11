from pathlib import Path
from Graph import Graph
import pandas as pd
import random
import math

data_path = "data"
random.seed(1234)


def generate_binomial_graph(num_vertices, num_edges):
    if num_edges > num_vertices * (num_vertices - 1) / 2:
        raise ValueError("Too many edges for the given number of nodes.")

    er_graph = Graph()
    for i in range(num_vertices):
        er_graph.add_vertex(i)

    edge_count = 0
    while edge_count < num_edges:
        node1, node2 = random.sample(range(num_vertices), 2)
        if (node1 != node2) and (node2 not in er_graph.adjacency_list[node1]):
            er_graph.add_edge(node1, node2)
            edge_count += 1

    return er_graph


def main():
    folder = Path(data_path)
    if folder.is_dir():

        table1_list = []

        for file in folder.iterdir():
            if file.is_file():
                language = file.name.split('_')[0]
                with open(file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    numbers = first_line.split()
                    vertices_num = int(numbers[0])
                    edges_num = int(numbers[1])
                    mean_degree = 2 * edges_num / vertices_num
                    delta = mean_degree / (vertices_num - 1)
                    df = pd.DataFrame(
                        {"Language": [language], "N": [vertices_num], "E": [edges_num], "k": [mean_degree],
                         "delta": [delta]})
                    table1_list.append(df)

        table1 = pd.concat(table1_list, ignore_index=True)
        print(table1)

    else:
        print("Directory not found.")


def generate_randomized_graph(graph, qe):
    random_graph = graph.copy()
    vertices = random_graph.get_vertices()

    for i in range(qe + 1):
        node11, node21 = random.sample(list(vertices), 2)
        if (node11 == node21):
            continue

        # Check is one of the selected nodes is not connected to any other vertex, and if so the iteration should not
        # count because the algorithm picks an edge not a node, but it had to be done like this due to the data structure
        if not random_graph.adjacency_list[node11] or not random_graph.adjacency_list[node21]:
            i -= 1
            continue

        node12 = random.sample(random_graph.adjacency_list[node11], 1)[0]
        node22 = random.sample(random_graph.adjacency_list[node21], 1)[0]
        # avoid self loops
        if (node11 == node22) or (node21 == node12) or (
                # avoid multi edges
                node22 in random_graph.adjacency_list[node11]) or (
                node12 in random_graph.adjacency_list[node21]):
            continue
        # Do de switching
        random_graph.adjacency_list[node11].append(node22)
        random_graph.adjacency_list[node11].remove(node12)

        random_graph.adjacency_list[node21].append(node12)
        random_graph.adjacency_list[node21].remove(node22)

    return random_graph


def test_basque():
    with open('data/Basque_syntactic_dependency_network.txt', 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        numbers = first_line.split()
        # vertices_num = int(numbers[0])
        # edges_num = int(numbers[1])

        graph = Graph()
        # Read the graph
        for line in f:
            values = line.strip().split()
            if len(values) == 2:
                graph.add_vertex(values[0])
                graph.add_vertex(values[1])
                graph.add_edge(values[0], values[1])

        n = graph.get_number_of_vertices()
        e = graph.get_number_of_edges()
        print(n)
        print(e)
        # print(graph.calculate_mean_closeness())

        # er_graph = generate_binomial_graph(n, e)

        er_graph = generate_binomial_graph(10, 5)
        print(er_graph.get_number_of_vertices())
        print(er_graph.get_number_of_edges())
        # print(er_graph.calculate_mean_closeness())

        qe = math.trunc(math.log(e) * e)
        print(qe)
        random_graph = generate_randomized_graph(er_graph, qe)

        print(random_graph.get_number_of_vertices())
        print(random_graph.get_number_of_edges())


if __name__ == "__main__":
    # main()
    test_basque()
