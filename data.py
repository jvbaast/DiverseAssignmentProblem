import generate_data
import timing_test, pareto_tests
import exact, algorithm,fileio

exact.setup_env()

sizes = [4, 8, 16, 32, 64, 128]
generate_data.generate_datasets(sizes) # Comment out if already generated