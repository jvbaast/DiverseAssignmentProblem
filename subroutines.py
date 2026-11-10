### File containing routines for solving subproblems used in the heuristic. 
### It contains cardinality-constrained matching, the (unbalanced) transportation problem
### and getting the dominating set from a set of points.

import networkx as nx
import numpy as np
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt

# Solves the k-cardinality constrained 2-matching problem
def solve_k_card_2_matching(matrix, k, maximize=True):

    matrix = np.asarray(matrix)
    n = len(matrix)
    total = np.sum(np.abs(matrix)) + 1 # Arbitrary big number

    # Initialize bipartite graph with 4n - 2k nodes
    graph = np.zeros((2*n - k, 2*n - k), dtype=int)
    graph[:n, :n] = matrix # real weights

    # Add dummy nodes
    graph[:n, n:] = total # high weight between real and dummys
    graph[n:, :n] = total 
    graph[n:, n:] = -total # low weigt between dummys

    # Solve assignment problem
    rows, cols = linear_sum_assignment(graph, maximize=maximize)

    # Create a dictionary of edges based on the resulting matching, where value is multiplicity
    result = {}
    for row, col in zip(rows, cols):
        if row < n and col < n:
            if row <= col:
                result[(row, col)] = result.get((row, col), 0) + 1
            else:
                result[(col, row)] = result.get((col, row), 0) + 1

    return result

# Solves the (unbalanced) transportation problem with certain supplies and demands
def solve_transportation(matrix, supplies, demands, maximize=True):
    matrix = np.asarray(matrix)

    L = np.repeat(np.arange(len(supplies)), supplies)
    R = np.repeat(np.arange(len(demands)), demands)

    transportation_matrix = matrix[np.ix_(L, R)]
    rows, cols = linear_sum_assignment(transportation_matrix, maximize=maximize)
    
    result = np.zeros(matrix.shape)
    np.add.at(result, (L[rows], R[cols]), 1)

    return result

# Get the dominating set from a set of points
def get_dominating_set(points):
    points.sort(reverse=True)
    max_y = points[0][1]
    dominating_set = [points[0]]
    for point in points[1:]:
        if point[1] > max_y:
            max_y = point[1]
            dominating_set += [point]
    return dominating_set

# Gets the minimum diversity weight in D=(R,B)
def get_minimum_diversity(D, n):

    # Calculate optimal 2-matching with inverse weights
    two_matching = solve_k_card_2_matching(D, n, maximize=False)

    # Calculate diversity
    diversity = 0
    for i in range(n):
        for j in range(i,n):
            if two_matching.get((i,j), 0) > 0:
                diversity += D[i][j] * int(two_matching[(i,j)])

    return diversity

# Gets the maximum diversity weight in D=(R,B)
def get_maximum_diversity(D, n):

    # Calculate optimal 2-matching with inverse weights
    two_matching = solve_k_card_2_matching(D, n)

    # Calculate diversity
    diversity = 0
    for i in range(n):
        for j in range(i,n):
            if two_matching.get((i,j), 0) > 0:
                diversity += D[i][j] * int(two_matching[(i,j)])

    return diversity

# Gets the minimum assignment weight in G=(L,A+B)
def get_minimum_cost(G, n):

    # Solve transportation
    supplies = 2 * np.ones(n, dtype=int)
    demands = 2 * np.ones(n, dtype=int)
    flow = solve_transportation(G, supplies, demands, maximize=False)

    # Calculate weight of matchings
    cost = 0
    for i in range(n):
        for j in range(n):
            cost += flow[i][j] * G[i][j]

    return cost

# Gets the maximum assignment weight in G=(L,A+B)
def get_maximum_cost(G, n):

    # Solve transportation
    supplies = 2 * np.ones(n, dtype=int)
    demands = 2 * np.ones(n, dtype=int)
    flow = solve_transportation(G, supplies, demands)

    # Calculate weight of matchings
    cost = 0
    for i in range(n):
        for j in range(n):
            cost += flow[i][j] * G[i][j]

    return cost