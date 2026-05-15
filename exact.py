### This file contains the ILP formulation of DAP and solves it using Gurobi.

import gurobipy as gp
from gurobipy import GRB
import numpy as np	
import subroutines

env = gp.Env(empty=True)

def setup_env():
    env.start()
    print()

# Solve ILP formulation of DAP
def solve_ip(G, D, n, min_div):
    model = gp.Model("IP", env=env)
    
    I = range(n)
    J = range(n)
    K = range(n)

    # Add variables x_ijk
    variables = model.addVars(I, J, K, vtype=GRB.BINARY, name="x")

    # For all i, add degree constraint
    for i in I:
        model.addConstr((gp.quicksum(variables[i,j,k] for j in J for k in K)) == 1, "c0,"+str(i))

    # For all j, add degree constraints
    for j in J:
        model.addConstr((gp.quicksum(variables[i,j,k] for i in I for k in K)) == 1, "c1,"+str(j))
        model.addConstr((gp.quicksum(variables[i,k,j] for i in I for k in K)) == 1, "c2,"+str(j))
    
    # Add diversity constraint
    model.addConstr((gp.quicksum(variables[i,j,k] * D[j][k] for i in I for j in J for k in K)) >= min_div, "c_div")

    # # Set objective
    model.setObjective(gp.quicksum(variables[i,j,k] * (G[i][j] + G[i][k]) for i in I for j in J for k in K), GRB.MAXIMIZE)

    model.optimize()

    # Read results from model
    try:
        assignment = np.zeros((n,n))
        for v in model.getVars():
            if v.X > 0.01:
                nums = [int(x) for x in v.VarName[2:-1].split(',')]
                assignment[nums[0]][nums[1]] += 1
                assignment[nums[0]][nums[2]] += 1
    except:
        print("Minimum diverstiy: " + str(min_div))
        raise Exception("Gurobi crashed")

    # Calculate diversity
    diversity = 0
    weight = 0
    for i in range(n):
        r = []
        for j in range(n):
            if assignment[i][j] > 0:
                r += [j] * int(assignment[i][j])
                weight += G[i][j] * int(assignment[i][j])
        diversity += D[r[0]][r[1]]

    return assignment, weight, diversity

# Function for recursively searching an interval (min_div,max_div) (non-inclusive) for a new solution.
# This function uses the fact that the IP uses a lower bound on the diversity, so the only criteria 
# for not being dominated by start or end is to not be equal to start and have better cost than end.
def search_interval_recursive(G, D, n, start, end, min_div, max_div):
    # Solve the IP for the middle value of (start, end)
    ass, cost, div = solve_ip(G, D, n, (min_div + max_div) / 2)

    # If the solution is not dominated by start or end, we return it
    if (cost != start[0] or div != start[1]) and (cost > end[0]):
        return (cost, div)
    # If the solution is different from start but not better than end, we decrease the lower bound on diversity.
    # Recursion stops if integer precision is reached.
    if (cost != start[0] or div != start[1]) and abs(max_div - min_div) > 0.5:
        return search_interval_recursive(G, D, n, start, end, min_div, (min_div + max_div) / 2)
    
    # If the solution is different from end but not from start, we increase the lower bound on diversity.
    # Recursion stops if integer precision is reached.
    if (cost != end[0] or div != end[1]) and abs(max_div - min_div) > 0.5:
        return search_interval_recursive(G, D, n, start, end, (min_div + max_div) / 2, max_div)
    return start

# Recursively calculate pareto front using exact algorithm
def get_pareto_front_recursive(G, D, n, start, end):
    result = []

    # Find a solution in the interval (start, end) (non-inclusive)
    # Here, start[1] and end[1] are the lower bound on diversity in the IP 
    sol = search_interval_recursive(G, D, n, start, end, start[1], end[1])

    # If the solution is different from start, we add it to the result
    if (sol[0] != start[0] or sol[1] != start[1]):
        result += [sol]
        # If the diversity is better than start, then (start, sol) can still contain solutions
        if (start[0] > sol[0]):
            result += get_pareto_front_recursive(G, D, n, start, sol)
        # (sol, end) can always contain more solutions
        result += get_pareto_front_recursive(G, D, n, sol, end)
    return result

# Calling function for recursive process
def get_pareto_front(G, D, n):
    # Get upper and lower bounds on diversity
    min_div = subroutines.get_minimum_diversity(D, n)
    max_div = subroutines.get_maximum_diversity(D, n)

    # Get upper and lower bounds and quality
    ass, max_cost, div = solve_ip(G, D, n, min_div)
    ass, min_cost, div = solve_ip(G, D, n, max_div)

    # Initialize list of solutions with upper and lower bounds
    result = [(max_cost, min_div), (min_cost, max_div)]

    # Start recursive procedure
    if max_cost > min_cost:
        result += get_pareto_front_recursive(G, D, n, (max_cost, min_div), (min_cost, max_div))

    # Filter out dominated points
    dominating_set = subroutines.get_dominating_set(result)
    return dominating_set
