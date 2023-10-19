import pandas as pd
import random
import math
import time
from pathlib import Path
from Graph import *
from experiments import *

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


def sort_adj_list(adj_list_dict, sort):
    if sort == "original":
        dict_list = adj_list_dict
    elif sort == "random":
        dict_list = sort_dict_randomly(adj_list_dict)
    elif sort == "inc_degree":
        dict_list = sort_dict_by_list_length_ascending(adj_list_dict)
    elif sort == "dec_degree":
        dict_list = sort_dict_by_list_length_descending(adj_list_dict)
    return list(dict_list.keys())


def monte_carlo_estimation(original_graph, t, m_max, exp_type, sort="original", c_lang=None):
    n = original_graph.get_number_of_vertices()
    e = original_graph.get_number_of_edges()
    qe = math.trunc(math.log(e) * e)

    # Different orderings
    adj_list_og = sort_adj_list(original_graph.adjacency_list, sort)

    counter = 0

    # Calculate the c for every m of the language graph only once and save it in a list
    # if c_lang is not None it was already computed (saves computational charge)
    if not c_lang:
        c_lang = []
        m_count = math.trunc(m_max * 0.1)
        node_index = c_og = 0
        while True:
            while node_index <= m_count:
                vertex = adj_list_og[node_index]
                distances = original_graph.bfs_distances(vertex)
                ci = 0
                for dij in distances.values():
                    if dij != 0:
                        ci += (1 / dij)
                c_og += (ci / (n - 1))
                node_index += 1
            c_lang.append(c_og / m_count)
            if m_max <= m_count:
                break
            m_count = (m_count * 2) if (m_count * 2 < m_max) else m_max

    print(c_lang[-1])
    print(f"Null model: {exp_type}")

    for i in range(t):
        if exp_type == "ER":
            random_graph = generate_binomial_graph(n, e)
        elif exp_type == "SWI":
            random_graph = generate_randomized_graph(original_graph, qe)
        print("Iteration ", i)

        adj_list_rand = sort_adj_list(random_graph.adjacency_list, sort)

        c_og_index = c_rand = 0
        m_count = math.trunc(m_max * 0.1)

        node_index = 0
        while True:
            while node_index <= m_count:
                # iterate over null graph
                vertex = adj_list_rand[node_index]
                distances = random_graph.bfs_distances(vertex)
                ci = 0
                for dij in distances.values():
                    if dij != 0:
                        ci += (1 / dij)

                c_rand += (ci / (n - 1))
                node_index += 1

            c_rand_min = c_rand / n
            c_rand_max = c_rand / n + 1 - m_count / n

            c_og_est = c_lang[c_og_index]

            # lower bound
            if c_rand_min >= c_og_est:
                print("break by lower bound")
                counter += 1
                break

            # upper bound
            if c_rand_max < c_og_est:
                print("break by upper bound")
                break

            # Max condition
            if m_max <= m_count:
                c_rand_est = c_rand / m_count
                print(f" m max achieved: c_rand_est: {c_rand_est} , c_og_est: {c_og_est}")
                # if c_rand_est >= c_og_est:
                if round(c_rand_est, 2) >= round(c_og_est, 2):
                    counter += 1
                break
            # Increment m until m_max
            m_count = m_count * 2 if (m_count * 2 < m_max) else m_max
            c_og_index += 1

    return counter / t, c_og_est, c_lang



def main():
    folder = Path(data_path)
    if folder.is_dir():
        table1_list = []
        table2_list = []
        for file in folder.iterdir():
            if file.is_file():
                language = file.name.split('_')[0]
                print("=" * 50)
                print(language)
                print("=" * 50)
                with open(file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    numbers = first_line.split()
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

                    # Calculate table 1
                    mean_degree = 2 * e / n
                    delta = mean_degree / (n - 1)
                    df1 = pd.DataFrame(
                        {"Language": [language], "N": [n], "E": [e], "k": [mean_degree],
                         "delta": [delta]})
                    table1_list.append(df1)

                    # Calculate table 2 (p-values)
                    m_max = math.trunc(n * 0.1)
                    t = 20
                    pv_switch, c, c_lang = monte_carlo_estimation(graph, t, m_max, "SWI", "random", None)
                    pv_bi, _, _ = monte_carlo_estimation(graph, t, m_max, "ER", "random", c_lang)

                    df2 = pd.DataFrame(
                        {"Language": [language], "Closeness": [c], "p-value (binomial)": [pv_bi],
                         "p-value (switching)": [pv_switch], })
                    table2_list.append(df2)
    else:
        print("Directory not found.")

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    table1 = pd.concat(table1_list, ignore_index=True)
    print("=" * 50)
    print("Table 1")
    print("=" * 50)
    print(table1)

    table2 = pd.concat(table2_list, ignore_index=True)
    print("=" * 50)
    print("Table 2")
    print("=" * 50)
    print(table2)



    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    table2 = pd.concat(table2_list, ignore_index=True)
    print("=" * 50)
    print("Table 2")
    print("=" * 50)
    print(table2)


if __name__ == "__main__":
    main()
