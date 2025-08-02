"""
messages.ipynb

This module provides functions and constants for formatting, generating, and writing status, error, and validation messages
to HTML and TXT result files for the SPI test platform. It supports colored output for both terminal and HTML, and includes
utility functions for initializing and closing result files, as well as for reporting the status of SPI command execution and data comparisons.

Main functionalities:
    - Define color and formatting templates for HTML and terminal messages.
    - Write status, error, and validation messages to result files.
    - Initialize and close HTML and TXT result files.
    - Provide utility functions for message formatting and output.

Intended usage:
    - Used throughout the test platform to provide consistent, human-readable feedback and logging.
    - Designed to be called by SPI command execution and comparison functions.

Dependencies:
    - Requires configuration dictionary (config.yaml) for color settings.
    - Relies on global flags for controlling output and exception behavior.
"""


# For HTML Result files 
##### Uncomment this to change the default color of msg

# Colors : can be changed in config file
text_colors = config["RESULT_FILE"]["html_config"]["text_colors"]
highlight_colors = config["RESULT_FILE"]["html_config"]["highlight_colors"]
start_p_html = f"<p style=\"color:{text_colors['default_color']};\">"
start_error_span = f"<span style=\"color:{text_colors['error_color']};  background-color: {highlight_colors['error_color']};\">"
start_valid_span = f"<span style=\"color:{text_colors['validation_color']}; background-color: {highlight_colors['validation_color']};\">"

end_cmp_div = "</div> \n"
end_span = "</span>"
end_p = "</p>"

error_msg_html = f"{start_error_span} ERROR : {end_span}"
valid_msg_html = f"{start_valid_span} SUCCESSFUL : {end_span}"
    
red_color = '\033[7;49;91m'
green_colour = '\033[7;49;32m'
normal_colour = '\033[0;5;49m'

error_msg = f"{red_color} ERROR : {normal_colour}"
valid_msg = f"{green_colour} SUCCESSFUL : {normal_colour}"