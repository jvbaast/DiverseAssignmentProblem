import exact, subroutines, fileio, algorithm
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scienceplots

# Calculate n+1 points using exact algorithm
# We do only n+1 points because so does the heuristic
def get_exact_points(G, D, n):
    result = []
    min_div = subroutines.get_minimum_diversity(D, n)
    max_div = subroutines.get_maximum_diversity(D, n)
    for i in range(n+1):
        ass, cost, div = exact.solve_ip(G, D, n, min_div + (i / n) * (max_div - min_div))
        result += [(cost, div)]
    dominating_set = subroutines.get_dominating_set(result)
    return dominating_set

# Timing test for exact and approximate algorithm
def run_timing_test_pareto(assignments, divs, sizes):
    inst = 0
    for size in sizes:
        fileio.create_empty_file("timing/pareto/approx/" + str(size))
        fileio.create_empty_file("timing/pareto/exact/" + str(size))
        for asgn in assignments:
            for div in divs:
                for i in range(10):
                    inst += 1
                    inst_name = div + "_" + str(asgn) + "_"+ str(size) + "_" + str(i)
                    print("\rRunning Pareto timing test: " + inst_name + " (" + str(inst) + "/" + str(10 * len(assignments) * len(sizes) * len(divs)) + ")", end='', flush=True)
                    (n, G, D) = fileio.load_file("data/" + inst_name)
                    start = time.process_time()
                    algorithm.get_algorithm_points(G, D, n)
                    end = time.process_time()
                    fileio.file_append_num("timing/pareto/approx/" + str(size), end - start)
                    start = time.process_time()
                    exact.get_pareto_front(G, D, n)
                    end = time.process_time()
                    fileio.file_append_num("timing/pareto/exact/" + str(size), end - start)
    print()

# Timing test for exact and approximate algorithm
def run_timing_test_instance(assignments, divs, sizes):
    inst = 0
    for size in sizes:
        fileio.create_empty_file("timing/inst/approx/" + str(size))
        fileio.create_empty_file("timing/inst/exact/" + str(size))
        for asgn in assignments:
            for div in divs:
                for i in range((1 + 10 // size)):
                    inst += 1
                    inst_name = div + "_" + str(asgn) + "_"+ str(size) + "_" + str(i)
                    print("\rRunning instance timing test: " + inst_name + " (" + str(inst) + "/" + str(10 * len(assignments) * len(sizes) * len(divs)) + ")", end='', flush=True)
                    (n, G, D) = fileio.load_file("data/" + inst_name)
                    start = time.process_time()
                    algorithm.get_algorithm_points(G, D, n)
                    end = time.process_time()
                    fileio.file_append_num("timing/inst/approx/" + str(size), (end - start) / (n+1))
                    start = time.process_time()
                    get_exact_points(G, D, n)
                    end = time.process_time()
                    fileio.file_append_num("timing/inst/exact/" + str(size), (end - start) / (n+1))
    print()

# Make plots of the running times in regular scale and log scale
def plot_timings(sizes):
    arr_inst_approx = []
    arr_inst_exact = []
    arr_pareto_approx = []
    arr_pareto_exact = []
    for size in sizes:
        timings = fileio.read_timings("timing/inst/approx/" + str(size))
        arr_inst_approx += [np.average(timings)]
        timings = fileio.read_timings("timing/inst/exact/" + str(size))
        arr_inst_exact += [np.average(timings)]
        timings = fileio.read_timings("timing/pareto/approx/" + str(size))
        arr_pareto_approx += [np.average(timings)]
        timings = fileio.read_timings("timing/pareto/exact/" + str(size))
        arr_pareto_exact += [np.average(timings)]

    plot_params = dict (
        xlabel="Size of instance", 
        ylabel="Running time (s)",
        xticks=sizes,
    )

    ### Switch styles if LaTeX is installed
    with plt.style.context(["science", "ieee"]):
    # with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots()
        ax.plot(sizes, arr_inst_approx, marker='s', ms=3, label="Approximation")
        ax.plot(sizes, arr_inst_exact, marker='s', ms=3, label="Exact")
        ax.set(**plot_params)
        ax.margins(0.05)
        ax.legend()
        fig.savefig("figures/timings_inst_linear.pdf", dpi=300)
        plt.close()

    ### Switch styles if LaTeX is installed
    with plt.style.context(["science", "ieee"]):
    # with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots()
        ax.plot(sizes, arr_inst_approx, marker='s', ms=3, label="Approximation")
        ax.plot(sizes, arr_inst_exact, marker='s', ms=3, label="Exact")
        # ax.set_xscale("log", base=2)
        ax.set_yscale("log", base=10)
        ax.set(**plot_params)
        ax.margins(0.05)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:.3g}'.format(y)))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:.3g}'.format(x)))
        ax.legend()
        fig.savefig("figures/timings_inst_log.pdf", dpi=300)
        plt.close()

    ### Switch styles if LaTeX is installed
    with plt.style.context(["science", "ieee"]):
    # with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots()
        ax.plot(sizes, arr_pareto_approx, marker='s', ms=3, label="Approximation")
        ax.plot(sizes, arr_pareto_exact, marker='s', ms=3, label="Exact")
        ax.set(**plot_params)
        ax.margins(0.05)
        ax.legend()
        fig.savefig("figures/timings_pareto_linear.pdf", dpi=300)
        plt.close()

    ### Switch styles if LaTeX is installed
    with plt.style.context(["science", "ieee"]):
    # with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots()
        ax.plot(sizes, arr_pareto_approx, marker='s', ms=3, label="Approximation")
        ax.plot(sizes, arr_pareto_exact, marker='s', ms=3, label="Exact")
        # ax.set_xscale("log", base=2)
        ax.set_yscale("log", base=10)
        ax.set(**plot_params)
        ax.margins(0.05)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:.3g}'.format(y)))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:.3g}'.format(x)))
        ax.legend()
        fig.savefig("figures/timings_pareto_log.pdf", dpi=300)
        plt.close()