import generate_data
import timing_test, pareto_tests
import exact, algorithm,fileio

exact.setup_env()

sizes = [64]
assignments = [100]
divs = ["uniform_div", "random_div"]

pareto_tests.run_test(assignments, divs, sizes) # Comment out if already run