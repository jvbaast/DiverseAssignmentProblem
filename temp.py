import fileio
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scienceplots

# Make plots of the running times in regular scale and log scale
def plot_points(points1, points2, name):
    plot_params = dict (
        xlabel="Quality", 
        ylabel="Diversity",
    )

    ### Switch styles if LaTeX is installed
    with plt.style.context(["science", "ieee"]):
        fig, ax = plt.subplots()
        ax.scatter(*zip(*points1), marker='s', s=3, label="$\\textsc{Alg}$")
        ax.scatter(*zip(*points2), marker='s', s=3, label="Exact")
        ax.set_ylim(ymin=0, ymax=68)
        ax.set_xlim(xmin=0, xmax=1350)
        # ax.margins(20)
        ax.set(**plot_params)
        ax.margins(0.05)
        ax.legend(loc='lower left')
        fig.savefig(name, dpi=300)
        plt.close()

plot_points(fileio.read_points("pareto/approx/disjoint_div_10_64_0")[1], fileio.read_points("pareto/exact/disjoint_div_10_64_0")[1],"figures/point_plot1.pdf")
plot_points(fileio.read_points("pareto/approx/random_div_100_64_9")[1], fileio.read_points("pareto/exact/random_div_100_64_9")[1],"figures/point_plot2.pdf")