from .reports_pkg import red_color, green_colour

def init_txt_result_file(test_file_name):
    """
    Initializes and opens a TXT result file for writing test results.

    Args:
        test_file_name (str): Name of the test file.
        test_file_path (str): Path to the test file.

    Returns:
        file object: Opened TXT file handle.
    """
    
    result_file_path_txt = "out/" + test_file_name + '_results.txt'
    result_file_txt = open(result_file_path_txt,"w")
    result_file_txt_title = f"Results from {test_file_name} \n \n"
    result_file_txt.write(result_file_txt_title)
    return result_file_txt

def end_txt_result_file(result_file_txt) -> None:
    """
    Writes the TXT footer and closes the TXT result file.
    """
    
    end_txt_file = "End of results for this file"
    result_file_txt.write(end_txt_file)
    result_file_txt.close()
    
    
def error_msg() -> str :
    """
    Returns the terminal formatted error message.

    Returns:
        str: Terminal string for an error message.
    """
    
    return f"{red_color} ERROR : "


def valid_msg() -> str :
    """
    Returns the terminal formatted validation message.

    Returns:
        str: Terminal string for a validation message.
    """
    
    return f"{green_colour} SUCCESSFUL : "