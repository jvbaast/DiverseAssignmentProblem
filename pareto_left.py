import generate_data
import timing_test, pareto_tests
import exact, algorithm,fileio

exact.setup_env()

# pareto_tests.process_pareto_file("random_div_10_64_5")
# pareto_tests.process_pareto_file("random_div_10_64_6")
# pareto_tests.process_pareto_file("random_div_10_64_7")
# pareto_tests.process_pareto_file("random_div_10_64_8")
# pareto_tests.process_pareto_file("random_div_10_64_9")
# pareto_tests.process_pareto_file("random_div_100_64_8")
# pareto_tests.process_approx_file("random_div_100_64_7")
pareto_tests.process_approx_file("random_div_100_64_9")
# pareto_tests.process_pareto_file("random_div_10_64_4")
# pareto_tests.process_pareto_file("random_div_100_64_7")
pareto_tests.process_pareto_file("random_div_100_64_9")