from pathlib import Path
from Graph import Graph
import pandas as pd

data_path = "data"


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

        # print(graph.get_number_of_vertices())
        # print(graph.get_number_of_edges())
        print(graph.calculate_mean_closeness())

if __name__ == "__main__":
    # main()
    test_basque()