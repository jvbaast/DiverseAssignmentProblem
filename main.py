import generate_data
import timing_test, pareto_tests
import exact, algorithm,fileio, subroutines

exact.setup_env()

sizes = [4, 8, 16, 32, 64]
assignments = [10, 100]
divs = ["disjoint_div", "distance_div", "uniform_div", "random_div"]

# generate_data.generate_datasets(sizes) # Comment out if already generated

pareto_tests.run_test(assignments, divs, sizes) # Comment out if already run
pareto_tests.calculate_pareto_stats(assignments, divs, sizes) # Results in pareto/stats folder

print()

timing_test.run_timing_test_pareto(assignments, divs, sizes) # Comment out if already run
timing_test.calculate_timing_stats(assignments, divs, sizes)
# timing_test.plot_timings(sizes)