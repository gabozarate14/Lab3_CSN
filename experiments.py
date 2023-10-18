from lab3 import *
import time
import math


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

