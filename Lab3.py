from pathlib import Path
from Graph import Graph
import pandas as pd
import random

data_path = "data"

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
                with open(file, 'r',encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    numbers = first_line.split()
                    vertices_num = int(numbers[0])
                    edges_num = int(numbers[1])
                    mean_degree = 2*edges_num/vertices_num
                    delta = mean_degree/(vertices_num-1)
                    df = pd.DataFrame(
                        {"Language": [language], "N": [vertices_num], "E": [edges_num], "k": [mean_degree],
                         "delta": [delta]})
                    table1_list.append(df)

        table1 = pd.concat(table1_list, ignore_index=True)
        print(table1)

    else:
        print("Directory not found.")


def test_basque():
    with open('data/Basque_syntactic_dependency_network.txt', 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        numbers = first_line.split()
        vertices_num = int(numbers[0])
        edges_num = int(numbers[1])

        graph = Graph()
        # Read the graph
        for line in f:
            values = line.strip().split()
            if len(values) == 2:
                graph.add_vertex(values[0])
                graph.add_vertex(values[1])
                graph.add_edge(values[0], values[1])

        print(graph.get_number_of_vertices())
        print(graph.get_number_of_edges())
        # print(graph.calculate_mean_closeness())

        num_vertices_er = graph.get_number_of_vertices()
        num_edges_er = graph.get_number_of_edges()
        er_graph = generate_binomial_graph(num_vertices_er, num_edges_er)
        print(er_graph.get_number_of_vertices())
        print(er_graph.get_number_of_edges())
        # print(er_graph.calculate_mean_closeness())



if __name__ == "__main__":
    # main()
    test_basque()