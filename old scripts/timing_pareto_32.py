import generate_data
import timing_test, pareto_tests
import exact, algorithm,fileio

exact.setup_env()

sizes = [32]
assignments = [10, 100]
divs = ["disjoint_div", "distance_div", "uniform_div", "random_div"]

timing_test.run_timing_test_pareto(assignments, divs, sizes) # Comment out if already run
timing_test.plot_timings(sizes)