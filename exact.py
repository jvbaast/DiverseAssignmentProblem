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
def solve_ip(G, D, n, alpha):
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
    
    model.setObjective(
        gp.quicksum(
            variables[i,j,k] * (alpha * (G[i][j] + G[i][k]) + (1-alpha) * D[j][k]) for i in I for j in J for k in K
        ), GRB.MAXIMIZE
    )
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
        print("Alpha value: " + str(alpha))
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

# Recursively calculate pareto front using exact algorithm
def get_pareto_front_recursive(G, D, n, start, end, depth):
    
    # Calculate new alpha such that both start and end have same value
    alpha = (end[1] - start[1]) / (start[0] - end[0] + end[1] - start[1])
    ass, cost, div = solve_ip(G, D, n, alpha)
    list1 = []; list2 = []

    # If new solution is different from both start and end, we recurse
    if (start[0] - cost > 0.5 or div - start[1] > 0.5) and (cost - end[0] > 0.5 or end[1] - div > 0.5):
        list1 = get_pareto_front_recursive(G, D, n, start, (cost, div, alpha), depth+1)
        list2 = get_pareto_front_recursive(G, D, n, (cost, div, alpha), end, depth+1)
    return list1 + list2 + [(cost, div)]

# Calling function for recursive process
def get_pareto_front(G, D, n):
    ass, cost1, div1 =  solve_ip(G, D, n, 1)
    ass, cost2, div2 =  solve_ip(G, D, n, 0)
    result = [(cost1, div1), (cost2, div2)]
    result += get_pareto_front_recursive(G, D, n, (cost1, div1, 1), (cost2, div2, 0), 0)
    dominating_set = subroutines.get_dominating_set(result)
    return dominating_set