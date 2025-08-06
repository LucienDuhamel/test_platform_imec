import package as pkg

from ..builder_html import (
    end_cmp_div,
    valid_msg_html,
    write_html_msg
)

from ..builder_print import valid_msg

def reg_cmp_match(result_file_html, result_file_txt, ref_data : str, rd_data : str) -> None :
    """
    Logs a successful register comparison.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        ref_data (str): Reference data string.
        rd_data (str): Read data string.
    """
    
    message = f""" **** Command #%4d: Last Reg read value (masked) = {rd_data}
    is equal to compared value =      {ref_data} **** \n """
    message_html = f""" 
    **** Command #%4d: Last Reg read value (masked) = {rd_data}
    is equal to compared value =                      {ref_data} **** 
    """
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
        
def mem_cmp_match(result_file_html, result_file_txt, ref_data : str, rd_data : str) -> None :
    """
    Logs a successful memory comparison.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        ref_data (str): Reference data string.
        rd_data (str): Read data string.
    """
    
    message = f""" **** Command #%4d: Last Mem read value = {rd_data}
    is equal to compared value =      {ref_data} **** \n """
    message_html = f""" 
    **** Command #%4d: Last Mem read value = {rd_data}
    is equal to compared value =             {ref_data} **** 
    """   
        
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
        
def valid_rd_msg(result_file_html, result_file_txt, indice_command_from_test_file, rd_tokens) :
    """
    Logs a successful read operation.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        indice_command_from_test_file: Index of the command in the test file.
        rd_tokens: Read data tokens.
    """
    
    message = f"Command # {indice_command_from_test_file}: Finished Reading; read value = {rd_tokens}  \n"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message)
        
def valid_wr_msg(result_file_html, result_file_txt, indice_command_from_test_file) :
    """
    Logs a successful write operation.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        indice_command_from_test_file: Index of the command in the test file.
    """
    
    message = f"Command # {indice_command_from_test_file}: Finished Writing  \n"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message)
    

def valid_cmp(result_file_html, result_file_txt, ref_data : list, rd_data : list) -> None:
    """
    Logs a successful data comparison.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        ref_data (list): Reference data list.
        rd_data (list): Read data list.
    """
    
    spaced_ref_data = ''
    spaced_rd_data = ''
    for data in ref_data :
        spaced_ref_data += data + ''
    for data in rd_data :
        spaced_rd_data += data + ''
        
    message = f"""The compared data are the same : {valid_msg()}
        the ref data is : {spaced_ref_data} 
        the read byte is : {spaced_rd_data} \n \n"""
    
    message_txt = f""" The compared data are the same : test SUCCESSFUL :
        the ref data is : {spaced_ref_data} 
        the read byte is : {spaced_rd_data} \n \n"""
        
    # Inside a <p>, use <br> to go to a new line 
    message_html = f""" 
    The compared data are the same : test {valid_msg_html()} <br> 
        the ref data is : {spaced_ref_data} <br>
        the tested data is : {spaced_rd_data} 
        """
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
        result_file_html.write(end_cmp_div()) # end the compare div