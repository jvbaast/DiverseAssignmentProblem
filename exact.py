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
            if v.X > 0.5:
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
    while max_cost - min_cost > 0.5:
        print("Costs: ", max_cost, min_cost, " Div: ", min_div)
        ass, cost, div = solve_ip(G, D, n, min_div + 1)
        result += [(cost, div)]
        min_div = div
        max_cost = cost

    # Filter out dominated points
    dominating_set = subroutines.get_dominating_set(result)
    return dominating_set
