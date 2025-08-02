# Tests if the given str argument is null or empty
# This function should be moved 
def is_empty(arg : str):
    if (arg is None or arg == ""):
        return True 
    
def test_length(result_file_html, result_file_txt, ref_length, length):
    if (ref_length != ref_length):
        wrong_wr_parameters(result_file_html, result_file_txt)   
    