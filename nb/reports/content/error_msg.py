import package as pkg

from ...nb_pkg import TextIO

from ..builder_html import (
    end_cmp_div,
    error_msg_html,
    write_html_msg
)

from ..builder_print import error_msg


def wrong_wr_parameters(result_file_html: TextIO, result_file_txt: TextIO) -> str:
    """
    Logs and returns a message for a mismatch in write command parameters.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.

    Returns:
        str: Error message.
    """
    
    message = "commands.yaml : mismatch between the given number of tokens for write command and the actual one in test file"
    wrong_config_parameters(result_file_html, result_file_txt, message)
    return message 

def test_config_error() -> None :
    """
    Raises an exception for an invalid test configuration (e.g., conflicting test flags).
    """
    message = f""" {error_msg()} Concurrency in the launch config : see the yaml file :  
                    single test and all_tests booleans should not have the same value ! \n"""
    raise Exception(message)
    
def number_of_bytes_mismatch(
    result_file_html: TextIO,
    result_file_txt: TextIO,
    nb_test_bytes : int,
    nb_rd_bytes : int,
) -> None :
    """
    Logs and optionally raises an error when the number of read bytes does not match the expected number.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        nb_test_bytes (int): Expected number of bytes.
        nb_rd_bytes (int): Actual number of bytes read.
    """
    
    message = f" {error_msg()} Both number of hex packets does not match : got {nb_rd_bytes}; should be {nb_test_bytes} \n"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        message_txt = f"ERROR : Both number of hex packets does not match : got {nb_rd_bytes}; should be {nb_test_bytes} \n"
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        message_html = f" {error_msg_html()} Both number of hex packets does not match : got {nb_rd_bytes}; should be {nb_test_bytes} \n"
        write_html_msg(result_file_html, message_html)
    if (pkg.activate_exceptions) :
        raise Exception(message)
        

def no_rd_data(result_file_html: TextIO, result_file_txt: TextIO) -> None :
    """
    Logs and optionally raises an error when no data has been read yet.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
    """
    
    message = f"{error_msg()} No data has been read yet. \n"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message)
    if (pkg.activate_result_file_html):
        message_html = f"{error_msg_html()} No data has been read yet. \n"
        write_html_msg(result_file_html, message_html)
    if (pkg.activate_exceptions) :
        raise Exception(message)

def unknown_cmd(result_file_html: TextIO, result_file_txt: TextIO, command : str) -> None :
    """
    Logs and optionally raises an error for an unknown command.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): The unknown command string.
    """
    
    message = f" {error_msg()} Unknown command: {command}"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        message_txt = f"ERROR : Unknown command: {command}"
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        message_html = f" {error_msg_html()} Unknown command: {command} \n"
        write_html_msg(result_file_html, message_html)
    if (pkg.activate_exceptions) :
        raise Exception(message)

def error_parsing_line(result_file_html: TextIO, result_file_txt: TextIO, line : str):
    """
    Logs and optionally raises an error when a line cannot be parsed.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        line (str): The problematic line.
    """
    
    message = f"{error_msg()} unable to parse line: {line}"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        message_txt = f"ERROR : unable to parse line: {line}"
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        message_html = f"{error_msg_html()} unable to parse line: {line} \n"
        write_html_msg(result_file_html, message_html)
    if (pkg.activate_exceptions) :
        raise Exception(message)
        

def wrong_config_parameters(result_file_html: TextIO, result_file_txt: TextIO, source: str) -> None:
    """
    Logs an error for wrong configuration parameters.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        source: Source or description of the configuration error.
    """
    message = f" {error_msg()} \t Wrong config parameters : see {source} . \n"
    message_txt = f" Error : Wrong config parameters : see {source} . \n"
    message_html = f" {error_msg_html()} \t Wrong config parameters : see {source} .\n"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
         
def error_wr_msg(result_file_html: TextIO, result_file_txt: TextIO, spi_cmd: str) -> None:
    """
    Logs an error message for a failed SPI write operation.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        spi_cmd: SPI command code.
    """
    message = f" {error_msg()} \t max number of while iterations reached during last writing operation. \n \t Searching for {spi_cmd}"
    message_txt = f" Error during last writing operation : max number of while iterations reached. \n \t Searching for {spi_cmd}"
    message_html = f" {error_msg_html()} \t max number of while iterations reached during last writing operation.\n \t Searching for {spi_cmd}"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
        
        
def error_rd_msg(result_file_html: TextIO, result_file_txt: TextIO, spi_cmd: str) -> None:
    """
    Logs an error message for a failed SPI read operation.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        spi_cmd: SPI command code.
    """
    message = f" {error_msg()} \t max number of while iterations reached during last reading operation. \n \t Searching for {spi_cmd}"
    message_txt = f" Error during last reading operation : max number of while iterations reached. \n \t Searching for {spi_cmd}"
    message_html = f" {error_msg_html()} \t max number of while iterations reached during last reading operation.\n \t Searching for {spi_cmd}"
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
        
    
def reg_cmp_mismatch(
    result_file_html: TextIO,
    result_file_txt: TextIO,
    ref_data : str,
    rd_data : str
) -> None :
    """
    Logs and optionally raises an error when register comparison fails.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        ref_data (str): Reference data string.
        rd_data (str): Read data string.
    """
    message = f""" **** {error_msg()} \t Command #%4d: Last Reg read value (masked) = {rd_data} 
                                                   is NOT EQUAL to compared value = {ref_data} **** \n """
    message_txt = f""" **** ERROR : \t Command #%4d: Last Reg read value (masked) = {rd_data} 
                                                   is NOT EQUAL to compared value = {ref_data} **** \n """
    message_html = f""" **** {error_msg_html()} \t Command #%4d: Last Reg read value (masked) = {rd_data} 
                                                             is NOT EQUAL to compared value = {ref_data} **** \n """
    
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
        
    if (pkg.activate_exceptions) :
        raise Exception(message)
        
def mem_cmp_mismatch(
    result_file_html: TextIO,
    result_file_txt: TextIO,
    ref_data : str,
    rd_data : str
) -> None :
    """
    Logs and optionally raises an error when memory comparison fails.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        ref_data (str): Reference data string.
        rd_data (str): Read data string.
    """
    
    message = f""" **** {error_msg()} \t Command #%4d: Last Mem read value = {rd_data} 
                                          is NOT EQUAL to compared value = {ref_data} **** \n """
    message_txt = f""" **** ERROR : \t Command #%4d: Last Mem read value = {rd_data} 
                                          is NOT EQUAL to compared value = {ref_data} **** \n """
    message_html = f""" **** {error_msg_html()} \t Command #%4d: Last Mem read value = {rd_data} 
                                                    is NOT EQUAL to compared value = {ref_data} **** \n """
    
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        write_html_msg(result_file_html, message_html)
        
    if (pkg.activate_exceptions) :
        raise Exception(message)
        
def invalid_cmp(
    result_file_html: TextIO,
    result_file_txt: TextIO,
    ref_data : str,
    rd_data : str
) -> None :
    """
    Logs and optionally raises an error when compared data do not match.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        ref_data (list): Reference data list.
        rd_data (list): Read data list.
    """
    
    # spaced_ref_data = ''
    # spaced_rd_data = ''
    # for data in ref_data :
    #     spaced_ref_data += data + ''
    # for data in rd_data :
    #     spaced_rd_data += data + ''
        
    message = f" \
    The compared data are not the same : {error_msg()} \n \
        the ref data is : {ref_data} \n \
        the tested byte is : {rd_data} \n "
    if (pkg.activate_msg_prints):
        print(message)
    if (pkg.activate_result_file_txt):
        message_txt = f" \
        The compared data are not the same : ERROR : \n \
            the ref data is : {ref_data} \n \
            the tested byte is : {rd_data} \n "
        result_file_txt.write(message_txt)
    if (pkg.activate_result_file_html):
        message_html = f""" 
        The compared data are not the same : test {error_msg_html()} <br> 
            the ref data is : {ref_data} <br> 
            the tested byte is : {rd_data} 
            """
        write_html_msg(result_file_html, message_html) 
        result_file_html.write(end_cmp_div()) # end the compare div
    
    if (pkg.activate_exceptions) :
        raise Exception(message)
  