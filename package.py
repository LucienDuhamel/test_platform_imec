from nb.reports.content import test_config_error
from nb.functions import load_config

config = load_config("config.yaml")

# Config setup
activate_exceptions = config["LAUNCH_CONFIG"]["activate_exceptions"]
max_while_iterations = config["LAUNCH_CONFIG"]["max_while_iterations"]

# Launch config : choose to run all tests (with exceptions) or run a single test : see config.yaml
single_test_config = config["LAUNCH_CONFIG"]["single_test"]
all_test_config = config["LAUNCH_CONFIG"]["all_tests"]
if (single_test_config["activate"] == all_test_config["activate"]):
    test_config_error()

# Result file config : choose the result file extension to be html or txt : see config.yaml
activate_result_file_html = config["RESULT_FILE"]["html_config"]["activate"]
activate_result_file_txt = config["RESULT_FILE"]["txt_config"]["activate"]
activate_msg_prints = config["RESULT_FILE"]["print_msg"]["activate"]