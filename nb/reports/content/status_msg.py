from ....package import (
    activate_msg_prints, 
    activate_result_file_html, 
    activate_result_file_txt
)

from ..builder_html import write_html_msg, start_cmp_div


def executing_line_msg(result_file_html, result_file_txt, line : str) -> None :
    """
    Logs the execution of a command line.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        line (str): command line which is currently executed.
    """
    
    message = f" {line}  \n " 
    if (activate_msg_prints):
        print(message)
    if (activate_result_file_txt):
        result_file_txt.write(message)
    if (activate_result_file_html):
        write_html_msg(result_file_html, message)


def sending_msg (result_file_html, result_file_txt, command : str, line : str, number_of_bytes : int) -> None :
    """
    Logs the sending of a command and its data.
    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): Command name.
        line (str): Data sent.
        number_of_bytes (int): Number of bytes in the data sent.
    """
    
    message = f"{command} ({number_of_bytes}) : {line} \n "
    if (activate_msg_prints):
        print(message)
    if (activate_result_file_txt):
        result_file_txt.write(message)
    if (activate_result_file_html):
        write_html_msg(result_file_html, message)
    
def starting_cmp(result_file_html, result_file_txt) -> None :
    """
    Logs the start of a data comparison section.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
    """
    
    message = f"Comparison of read data and reference data \n" 
    if (activate_msg_prints):
        print(message)
    if (activate_result_file_txt):
        message_txt = f" \n Comparison of read data and reference data \n" 
        result_file_txt.write(message_txt)
    if (activate_result_file_html):
        html_cmp = start_cmp_div()
        result_file_html.write(html_cmp) 