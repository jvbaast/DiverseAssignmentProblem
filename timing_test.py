import exact, subroutines, fileio, algorithm
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scienceplots

# Timing test for exact and approximate algorithm
def run_timing_test_pareto(assignments, divs, sizes):
    inst = 0
    for size in sizes:
        for asgn in assignments:
            for div in divs:
                for i in range(10):
                    inst += 1
                    inst_name = div + "_" + str(asgn) + "_"+ str(size) + "_" + str(i)
                    print("\rRunning Pareto timing test: " + inst_name + " (" + str(inst) + "/" + str(10 * len(assignments) * len(sizes) * len(divs)) + ")", end='', flush=True)
                    (n, G, D) = fileio.load_file("data/" + inst_name)
                    start = time.time()
                    algorithm.get_algorithm_points(G, D, n)
                    end = time.time()
                    fileio.write_num("timing/pareto/approx/" + inst_name, end - start)
                    start = time.time()
                    exact.get_pareto_front(G, D, n)
                    end = time.time()
                    fileio.write_num("timing/pareto/exact/" + inst_name, end - start)
    print()

# Calculate summary of stats
def calculate_timing_stats(assignments, divs, sizes):
    timings_approx = []
    timings_exact = []
    inst = 0
    for asgn in assignments:
        for div in divs:
            total_approx = []
            total_exact = []
            for size in sizes:
                total_approx += [0]
                total_exact += [0]
                for i in range(10):
                    inst += 1
                    inst_name = div + "_" + str(asgn) + "_"+ str(size) + "_" + str(i)
                    print("\rCalculating timing statistics: " + inst_name + " (" + str(inst) + "/" + str(10 * len(assignments) * len(sizes) * len(divs)) + ")", end='', flush=True)
                    approx = fileio.read_point_float("timing/pareto/approx/" + inst_name)
                    exact = fileio.read_point_float("timing/pareto/exact/" + inst_name)

                    total_approx[-1] += approx             
                    total_exact[-1] += exact         
                total_approx[-1] /= 10
                total_exact[-1] /= 10
            timings_approx += [total_approx]
            timings_exact += [total_exact]
    fileio.write_array("timing/stats/points_approximation", timings_approx)
    fileio.write_array("timing/stats/points_exact", timings_exact)
    print()