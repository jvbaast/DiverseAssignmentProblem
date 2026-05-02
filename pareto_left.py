import generate_data
import timing_test, pareto_tests
import exact, algorithm,fileio

exact.setup_env()

pareto_tests.process_pareto_file("distance_div_100_64_8")
pareto_tests.process_pareto_file("distance_div_100_64_9")
pareto_tests.process_pareto_file("distance_div_100_64_7")