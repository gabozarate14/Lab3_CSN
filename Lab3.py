from pathlib import Path
from Graph import Graph
import pandas as pd
import random
import math
import time

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


def exp_execution_time(graph):
    n = graph.get_number_of_vertices()
    e = graph.get_number_of_edges()
    er_graph = generate_binomial_graph(n, e)

    # Execution time experimentation
    start_time = time.time()
    c = er_graph.calculate_mean_closeness()
    print(f"Real Closeness: {c}")
    end_time1 = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time1 - start_time
    print(f"Execution time: {elapsed_time:.6f} seconds")

    m_max = math.trunc(n * 0.1)
    sum_est_c = er_graph.estimate_closeness_sum(m_max=m_max, sort="original")
    print(sum_est_c)

    c_est = sum_est_c / m_max
    print(f"Estimated Closeness: {c_est}")
    end_time2 = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time2 - end_time1
    print(f"Execution time: {elapsed_time:.6f} seconds")

    c_est_min = sum_est_c / n
    c_est_max = c_est_min + 1 - m_max / n

    print(f"Estimated Min Closeness: {c_est_min}")
    print(f"Estimated Max Closeness: {c_est_max}")


def exp_orderings(graph):
    n = graph.get_number_of_vertices()
    e = graph.get_number_of_edges()
    # er_graph = generate_binomial_graph(n, e)
    er_graph = graph

    print("=" * 50)
    print("Ordering Experimentation Report")
    print("=" * 50)
    t1 = time.time()
    c = er_graph.calculate_mean_closeness()
    print(f"Real Closeness: {c}")
    t2 = time.time()
    elapsed_time = t2 - t1
    print(f"Execution time: {elapsed_time:.6f} seconds")
    print("-" * 50)

    m_max = math.trunc(n * 0.1)

    sum_est_c = er_graph.estimate_closeness_sum(m_max=m_max, sort="original")
    c_est = sum_est_c / m_max
    print(f"Estimated Closeness Original ordering: {c_est}")
    t3 = time.time()
    elapsed_time = t3 - t2
    print(f"Execution time: {elapsed_time:.6f} seconds")
    print("-" * 50)

    results_random = []
    times_random = []
    for _ in range(11):
        sum_est_c = er_graph.estimate_closeness_sum(m_max=m_max, sort="random")
        c_est = sum_est_c / m_max
        t4 = time.time()
        elapsed_time = t4 - t3
        results_random.append(c_est)
        times_random.append(elapsed_time)
        t3 = t4

    c_est = sum(results_random) / len(results_random)
    print(f"Estimated Closeness Random ordering: {c_est}")
    elapsed_time = sum(times_random) / len(times_random)
    print(f"Execution time: {elapsed_time:.6f} seconds")
    print("-" * 50)

    sum_est_c = er_graph.estimate_closeness_sum(m_max=m_max, sort="inc_degree")
    c_est = sum_est_c / m_max
    print(f"Estimated Closeness Increasing Degree ordering: {c_est}")
    t5 = time.time()
    elapsed_time = t5 - t4
    print(f"Execution time: {elapsed_time:.6f} seconds")
    print("-" * 50)

    sum_est_c = er_graph.estimate_closeness_sum(m_max=m_max, sort="dec_degree")
    c_est = sum_est_c / m_max
    print(f"Estimated Closeness Decreasing Degree ordering: {c_est}")
    t6 = time.time()
    elapsed_time = t6 - t5
    print(f"Execution time: {elapsed_time:.6f} seconds")
    print("-" * 50)


def monte_carlo_method(original_graph, original_closeness, t, exp_type):

    n = original_graph.get_number_of_vertices()
    e = original_graph.get_number_of_edges()
    m_max = math.trunc(n * 0.1)
    qe = math.trunc(math.log(e) * e)

    print("Original closeness: ", original_closeness)
    counter = 0
    print(f"Monte Carlo method - {exp_type}")

    for i in range(t + 1):
        if exp_type == "ER":
            random_graph = generate_binomial_graph(n, e)
        elif exp_type == "SWI":
            random_graph = generate_randomized_graph(original_graph, qe)
        print("Iteration ", i)

        sum_est_c = random_graph.estimate_closeness_sum(m_max=m_max, sort="random")
        min_random_closeness = sum_est_c / n
        print("Min random closeness: ", min_random_closeness)

        if min_random_closeness >= original_closeness:
            counter += 1

    return counter / t

def exp_optimization(graph):
    t1 = time.time()
    print(f"Real Closeness: {graph.calculate_mean_closeness()}")
    t2 = time.time()
    elapsed_time = t2 - t1
    print(f"Execution time: {elapsed_time:.6f} seconds")

    t1 = time.time()
    print(f"Real Closeness Optimized: {graph.calculate_mean_closeness_optimized()}")
    t2 = time.time()
    elapsed_time = t2 - t1
    print(f"Execution time: {elapsed_time:.6f} seconds")

def exp_generate_hnull_graphs(graph):
    n = graph.get_number_of_vertices()
    e = graph.get_number_of_edges()

    m_max = math.trunc(n * 0.1)
    qe = math.trunc(math.log(e) * e)

    er_graph = generate_binomial_graph(n, e)
    print(er_graph.adjacency_list)
    random_graph = generate_randomized_graph(graph, qe)
    print(random_graph.adjacency_list)


def test_basque():
    with open('data/Basque_syntactic_dependency_network.txt', 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()

        graph = Graph()
        # Read the graph
        for line in f:
            values = line.strip().split()
            if len(values) == 2:
                graph.add_vertex(values[0])
                graph.add_vertex(values[1])
                graph.add_edge(values[0], values[1])

        # Experimentations
        exp_generate_hnull_graphs(graph)
        exp_optimization(graph)
        exp_execution_time(graph)
        exp_orderings(graph)

        # T = 50
        # p_value = monte_carlo_method(graph, n, e, T)
        # print("p-value is; ", p_value)

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
                    # ignore the shown nodes and edges because they change when self loops are deleted
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

                    # Calculate table 1
                    mean_degree = 2 * e / n
                    delta = mean_degree / (n - 1)
                    df1 = pd.DataFrame(
                        {"Language": [language], "N": [n], "E": [e], "k": [mean_degree],
                         "delta": [delta]})
                    table1_list.append(df1)

                    # Calculate table 2 (p-values)
                    m_max = math.trunc(n * 0.1)
                    t = 50
                    sum_est_c = graph.estimate_closeness_sum_optimized(m_max=m_max, sort="random")
                    c = sum_est_c / m_max
                    pv_bi = monte_carlo_method(graph, c, t, "ER")
                    pv_switch = monte_carlo_method(graph, c, t, "SWI")

                    df2 = pd.DataFrame(
                        {"Language": [language], "Closeness": [c], "p-value (binomial)": [pv_bi],
                         "p-value (switching)": [pv_switch]})
                    table2_list.append(df2)
    else:
        print("Directory not found.")

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


if __name__ == "__main__":
    # main()
    test_basque()
