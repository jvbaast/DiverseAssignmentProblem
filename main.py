import generate_data
import timing_test, pareto_tests
import exact, algorithm,fileio, subroutines

exact.setup_env()

inst_name = "uniform_div_100_64_6"
(n, G, D) = fileio.load_file("data/" + inst_name)

min_div = subroutines.get_minimum_diversity(D, n)
max_div = subroutines.get_maximum_diversity(D, n)

# Get upper and lower bounds and quality
ass, max_cost, div = exact.solve_ip(G, D, n, min_div)
ass, min_cost, div = exact.solve_ip(G, D, n, max_div)

# exact.get_pareto_front(G, D, n)

# sizes = [64]

# # generate_data.generate_datasets(sizes) # Comment out if already generated

# assignments = [100]
# divs = ["uniform_div", "random_div"]

# pareto_tests.run_test(assignments, divs, sizes) # Comment out if already run
# pareto_tests.calculate_pareto_stats(assignments, divs, sizes) # Results in pareto/stats folder

# sizes = [4, 8, 16, 32, 64]
# assignments = [10, 100]
# divs = ["disjoint_div", "distance_div", "uniform_div", "random_div"]
# # print()

# timing_test.run_timing_test_pareto(assignments, divs, sizes) # Comment out if already run
# timing_test.calculate_timing_stats(assignments, divs, sizes)
# # timing_test.plot_timings(sizes)