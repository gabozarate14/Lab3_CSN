from lab3 import *
import time
import math
import pandas as pd
from pathlib import Path
from Graph import *
from experiments import *


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


def exp_montecarlo(graph):
    n = graph.get_number_of_vertices()
    e = graph.get_number_of_edges()
    m_max = math.trunc(n * 0.1)
    sum_est_c = graph.estimate_closeness_sum_optimized(m_max=m_max, sort="random")
    c = sum_est_c / m_max
    t = 50
    pval, avg = monte_carlo_method(graph, c, t, "ER")
    print("=" * 50)
    print(f"Final p-value: {pval}, Avr. C: {avg}")
    pval, avg = monte_carlo_method(graph, c, t, "SWI")
    print("=" * 50)
    print(f"Final p-value: {pval}, Avr. C: {avg}")

def estimate_margin(graph, creal):

    n = graph.get_number_of_vertices()
    m_max = math.trunc(n * 0.1)
    n_exp = 20
    margin_list = []
    for _ in range(n_exp):
        sum_est_c = graph.estimate_closeness_sum_optimized(m_max=m_max, sort="random")
        cest = sum_est_c / m_max
        margin = abs(creal-cest)
        print(f"cest: {cest} - margin: {margin}")
        margin_list.append(margin)

    avg_margin = sum(margin_list)/len(margin_list)
    print(f"Estimated margin error when estimating: {avg_margin}")

def exp_orderings(graph):
    n = graph.get_number_of_vertices()
    e = graph.get_number_of_edges()

    t = 5
    m_max = math.trunc(n * 0.1)

    print("=" * 50)
    print("Ordering Experimentation Report")
    print("=" * 50)
    for sort in ["original", "random", "inc_degree", "dec_degree"]:
        t1 = time.time()
        p_val = monte_carlo_estimation(graph, t, m_max, "SWI", sort)
        print("SWI p-value is; ", p_val)
        t2 = time.time()
        elapsed_time = t2 - t1
        print(f"Execution time of {sort}: {elapsed_time:.6f} seconds")
        print("-" * 50)



def exp_small_graphs():
    folder = Path(data_path)
    if folder.is_dir():
        table2_list = []
        real_c = {"Basque": 0.269735556,
                  "Greek": 0.314726435,
                  "Italian": 0.327825244}

        for file in folder.iterdir():
            if file.is_file():
                language = file.name.split('_')[0]
                if language not in ['Basque', 'Greek', 'Italian']:
                    continue
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
                    # c = graph.calculate_mean_closeness_optimized()
                    c = real_c[language]
                    estimate_margin(graph, c)
                    df2 = pd.DataFrame(
                        {"Language": [language], "Closeness": [c]})
                    table2_list.append(df2)
    else:
        print("Directory not found.")

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

        n = graph.get_number_of_vertices()
        e = graph.get_number_of_edges()
        # Experimentations
        # exp_generate_hnull_graphs(graph)
        # exp_optimization(graph)
        # exp_execution_time(graph)
        # exp_montecarlo(graph)
        # p_value = monte_carlo_method(graph, n, e, T)
        # print("p-value is; ", p_value)
        # estimate_margin(graph)
        t = 20
        m_max = math.trunc(n * 0.1)
        # p_val = monte_carlo_estimation(graph, t, m_max, "ER", "original")
        # print("ER p-value is; ", p_val)
        p_val, c_est = monte_carlo_estimation(graph, t, m_max, "SWI", "random")
        print(f"SWI: p-value is: {p_val}, c est: {c_est}")
        # exp_orderings(graph)

def monte_carlo_method(original_graph, original_closeness, t, exp_type):
    tolerated_difference = 0.013
    n = original_graph.get_number_of_vertices()
    e = original_graph.get_number_of_edges()
    m_max = math.trunc(n * 0.1)
    qe = math.trunc(math.log(e) * e)

    print("Original closeness: ", original_closeness)
    counter = 0
    print(f"Monte Carlo method - {exp_type}")


    sum_c = []
    for i in range(t + 1):
        if exp_type == "ER":
            random_graph = generate_binomial_graph(n, e)
        elif exp_type == "SWI":
            random_graph = generate_randomized_graph(original_graph, qe)
        print("Iteration ", i)

        sum_est_c = random_graph.estimate_closeness_sum(m_max=m_max, sort="random")
        # min_random_closeness = sum_est_c / n
        random_closeness = sum_est_c / m_max
        print("Min random closeness: ", random_closeness)
        sum_c.append(random_closeness)
        if abs(random_closeness - original_closeness) <= tolerated_difference:
            counter += 1

    avg_c = sum(sum_c) / len(sum_c)

    return counter / t, avg_c


if __name__ == "__main__":
    test_basque()
    exp_small_graphs()