"""
translator.ipynb

This module provides a set of functions to parse, execute, and validate SPI (Serial Peripheral Interface) commands for a test platform.
It supports reading and writing to registers and memory, as well as comparing read data against reference values.
The results of each operation can be logged to both HTML and TXT result files for reporting and debugging purposes (see config.yaml file to configure the way these files are built).

Main functionalities:
    - Execute SPI commands parsed from a test file (REGRD, REGWR, MEMRD, MEMWR, MEMRDM, MEMWRM, REGCMP, MEMCMP).
    - Perform SPI read and write transactions.
    - Compare register and memory data with reference values (using masks for regs).
    - Log all actions and results in a human-readable format.

Intended usage:
    - Used as part of an automated test platform for SPI devices.
    - Functions are designed to be called with parsed command lines and maintain state between operations.

Dependencies:
    - Assumes existence of SPI interface object (spi_handler defined in main) and several helper functions for formatting, parsing, and messaging.
    - Relies on global configuration variables for command codes and data formatting.

Author: [Lucien Duhamel]
Date: [2025-07-29]
"""
import package as main_pkg

from . import formater as formater
from .functions import is_empty
from . import nb_pkg as nb_pkg


from .reports.content import status_msg, error_msg, valid_msg
from . import reports as reports
from . import spi

def command_disjunction(
    spi_handler: nb_pkg.SPI_Object, 
    result_file_html: nb_pkg.TextIO, 
    result_file_txt: nb_pkg.TextIO, 
    indice_command_from_test_file : int, 
    parsed_line : list, 
    last_rd_data : list,
) -> list[int]|None :
    """
    Executes the appropriate SPI command based on the parsed command line.

    Handles commands such as REGRD, REGWR, MEMRD, MEMWR, MEMRDM, MEMWRM, REGCMP, and MEMCMP.
    Updates last_rd_data for read commands and performs comparisons for CMP commands.

    Args:
        spi_handler: SPI interface object.
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        indice_command_from_test_file (int): Index of the command in the test file.
        parsed_line (list): Parsed command and its arguments.
        last_rd_data (list): Data read from the last read command.

    Returns:
        list: Updated last_rd_data after command execution.
    """
    formated_line = formater.format_parsed_line(parsed_line)
    status_msg.executing_line_msg(result_file_html, result_file_txt, formated_line)
    
    command = parsed_line[0]
    if ((command == "REGRD" )):
        spi_cmd = nb_pkg.commands["REGRD"]["spi_pattern"]
        rd_addr = parsed_line[1]
        last_rd_data = rd_transaction_behaviour(spi_handler, result_file_html, result_file_txt, indice_command_from_test_file, command, spi_cmd, rd_addr)

    elif ((command == "REGWR" )):
        spi_cmd = nb_pkg.commands["REGWR"]["spi_pattern"]
        wr_addr = parsed_line[1]
        wr_data = parsed_line[2]
        wr_transaction_behaviour(spi_handler, result_file_html, result_file_txt, indice_command_from_test_file, command, spi_cmd, wr_addr, wr_data)

    elif (command == "MEMRD") :
        spi_cmd = nb_pkg.commands["MEMRD"]["spi_pattern"]
        rd_addr = parsed_line[1]
        last_rd_data = rd_transaction_behaviour(spi_handler, result_file_html, result_file_txt, indice_command_from_test_file, command, spi_cmd, rd_addr)

    elif (command == "MEMWR"):
        spi_cmd = nb_pkg.commands["MEMWR"]["spi_pattern"]
        wr_addr = parsed_line[1]
        wr_data = parsed_line[2]
        wr_transaction_behaviour(spi_handler, result_file_html, result_file_txt, indice_command_from_test_file, command, spi_cmd, wr_addr, wr_data)

    elif (command == "MEMRDM") :
        spi_cmd = nb_pkg.commands["MEMRDM"]["spi_pattern"]
        rd_addr = parsed_line[1] # <=> None here
        last_rd_data = rd_transaction_behaviour(spi_handler, result_file_html, result_file_txt, indice_command_from_test_file, command, spi_cmd, rd_addr)

    elif (command == "MEMWRM") :
        spi_cmd = nb_pkg.commands["MEMWRM"]["spi_pattern"]
        wr_addr = parsed_line[1] # <=> None here
        wr_data = parsed_line[2] # <=> None here
        wr_transaction_behaviour(spi_handler, result_file_html, result_file_txt, indice_command_from_test_file, command, spi_cmd, wr_addr, wr_data)

    elif (command == "REGCMP"):
        ref_packets = parsed_line[2] 
        ref_mask = ref_packets[::nb_pkg.nb_token_to_compare_reg_cmp]
        ref_data = ref_packets[nb_pkg.nb_token_to_compare_reg_cmp::]
        
        if (is_empty(last_rd_data)):
            error_msg.no_rd_data(result_file_html, result_file_txt)
        else :
            reg_cmp_behaviour(result_file_html, result_file_txt, ref_mask, ref_data, last_rd_data)
            
    elif (command == "MEMCMP"):
        data_ref = parsed_line[2] 
        if (is_empty(last_rd_data)):
            error_msg.no_rd_data(result_file_html, result_file_txt)
        else :
            mem_cmp_behaviour(result_file_html, result_file_txt, data_ref, last_rd_data)

    else :
        error_msg.unknown_cmd(result_file_html, result_file_txt, command)
    return last_rd_data



def rd_transaction_behaviour(
    spi_handler: nb_pkg.SPI_Object,
    result_file_html: nb_pkg.TextIO,
    result_file_txt: nb_pkg.TextIO,
    indice_command_from_test_file: int,
    command: str,
    spi_cmd: int,
    rd_addr: list,
) -> list[int]:
    """
    Executes a read transaction over SPI, formats and reports the read data.

    Args:
        spi_handler: SPI interface object.
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        indice_command_from_test_file (int): Index of the command in the test file.
        command (str): Command name.
        spi_cmd (int): SPI command code.
        rd_addr (list): Address to read from.

    Returns:
        list: Data read from SPI.
    """
    valid_rd, rd_line = rd_spi_transaction(spi_handler, result_file_html, result_file_txt, command, spi_cmd, rd_addr)
    nb_hex_per_token_data = nb_pkg.nb_bytes_per_token_data * 2 # because one byte = 2 hex char
    formated_rd_line = formater.format_rd_data(rd_line, nb_hex_per_token_data)
    if valid_rd :
        valid_msg.valid_rd_msg(result_file_html, result_file_txt, indice_command_from_test_file, formated_rd_line)
    else :
        spi_cmd_hex = formater.from_int_to_hex(spi_cmd)
        error_msg.error_rd_msg(result_file_html, result_file_txt, spi_cmd_hex)
    return rd_line
        
        
def wr_transaction_behaviour(
    spi_handler: nb_pkg.SPI_Object,
    result_file_html: nb_pkg.TextIO,
    result_file_txt: nb_pkg.TextIO,
    indice_command_from_test_file : int,
    command : str,
    spi_cmd : int,
    wr_addr : list,
    wr_data : list,
) -> None:
    """
    Executes a write transaction over SPI.

    Args:
        spi_handler: SPI interface object.
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        indice_command_from_test_file (int): Index of the command in the test file.
        command (str): Command name.
        spi_cmd (int): SPI command code.
        wr_addr (list): Address to write to.
        wr_data (list): Data to write.

    Returns:
        None
    """
    valid_wr = wr_spi_transaction(spi_handler, result_file_html, result_file_txt, command, spi_cmd, wr_addr, wr_data)
    if valid_wr :
        valid_msg.valid_wr_msg(result_file_html, result_file_txt, indice_command_from_test_file)
    else :
        spi_cmd_hex = formater.from_int_to_hex(spi_cmd)
        error_msg.error_wr_msg(result_file_html, result_file_txt, spi_cmd_hex)





def reg_cmp_behaviour(
    result_file_html: nb_pkg.TextIO,
    result_file_txt: nb_pkg.TextIO,
    ref_mask : list,
    ref_data : list,
    last_rd_data : list
) -> None :
    """
    Compares register data read from SPI with reference data using a mask (only masked bytes are compared).

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): Command name.
        ref_mask (list): Mask to apply to reference data.
        ref_data (list): Reference data to compare.
        last_rd_data (list): Data read from SPI.

    Returns:
        None
    """
    status_msg.starting_cmp(result_file_html, result_file_txt)
    storage = "reg"
    
    # Data formatting to be able to compare
    parsed_ref_mask: list[int] = formater.parse_list_of_packets(ref_mask, "int")
    parsed_ref_data: list[int] = formater.parse_list_of_packets(ref_data, "int")
    
    nb_rd_bytes = len(last_rd_data)
    len_ref_data = len(parsed_ref_data)
    test_result = "valid"
    if (nb_rd_bytes != len_ref_data): 
        # print("these are the data mismatch :", ref_data, last_rd_data)
        error_msg.number_of_bytes_mismatch(result_file_html, result_file_txt, len_ref_data, nb_rd_bytes)
        test_result = "error"
    else :
        for byte_cnt in range(len_ref_data):
            # if the mask is not 0, we compare the data
            if (parsed_ref_mask[byte_cnt] & parsed_ref_data[byte_cnt] != 0):
                # we compare only data bytes : not mask bytes
                ref_byte: int = parsed_ref_data[byte_cnt]
                rd_byte:  int = last_rd_data[byte_cnt]
                
                one_byte_test_result = equal_bytes(result_file_html, result_file_txt, ref_byte, rd_byte, storage)
                if not one_byte_test_result :
                    test_result = "error"
                
    nb_hex_per_token_data = nb_pkg.nb_bytes_per_token_data * 2          
    formated_ref_data: str = formater.format_rd_data(parsed_ref_data, nb_hex_per_token_data)
    formated_rd_data:  str = formater.format_rd_data(last_rd_data, nb_hex_per_token_data)
    if (test_result == "valid"):    
        valid_msg.valid_cmp(result_file_html, result_file_txt, formated_ref_data, formated_rd_data)
    else :
        error_msg.invalid_cmp(result_file_html, result_file_txt, formated_ref_data, formated_rd_data)
        

def mem_cmp_behaviour(
    result_file_html: nb_pkg.TextIO,
    result_file_txt: nb_pkg.TextIO,
    ref_data : list[str],
    last_rd_data : list[int]
) -> None :
    """
    Compares memory data read from SPI with reference data.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): Command name.
        data_ref (list): Reference data to compare.
        last_rd_data (list): Data read from SPI.

    Returns:
        None
    """
    status_msg.starting_cmp(result_file_html, result_file_txt)
    storage = "mem"
    
    parsed_ref_data: list[int] = formater.parse_list_of_packets(ref_data, "int")
    nb_rd_bytes = len(last_rd_data)
    len_ref_data = len(parsed_ref_data)
    test_result = True
    if (len_ref_data != nb_rd_bytes): 
        # print("these are the number of bytes mismatch :", len_ref_data, nb_rd_bytes)
        error_msg.number_of_bytes_mismatch(result_file_html, result_file_txt, len_ref_data, nb_rd_bytes)
        test_result = False
    else :
        #Here from the MSB to the LSB 
        for token_cnt in range(len_ref_data):
            rd_token : int = last_rd_data[token_cnt]
            ref_token: int = parsed_ref_data[token_cnt]
            one_byte_test_result = equal_bytes(result_file_html, result_file_txt, ref_token, rd_token, storage)
            if not one_byte_test_result:
                test_result = False
    
    nb_hex_per_token_data = nb_pkg.nb_bytes_per_token_data * 2           
    formated_ref_data: str = formater.list_to_string(ref_data)
    formated_rd_data:  str = formater.format_rd_data(last_rd_data, nb_hex_per_token_data)
    if (test_result):    
        valid_msg.valid_cmp(result_file_html, result_file_txt, formated_ref_data, formated_rd_data)
    else :
        error_msg.invalid_cmp(result_file_html, result_file_txt, formated_ref_data, formated_rd_data)
    

def equal_bytes(
    result_file_html: nb_pkg.TextIO,
    result_file_txt: nb_pkg.TextIO,
    ref_byte : int,
    rd_byte : int,
    storage : str
) -> bool :
    """
    Compares two bytes and logs the result.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        ref_byte (int): Reference byte.
        rd_byte (int): Read byte.
        storage (str): Type of storage ('reg' or 'mem').

    Returns:
        bool: True if bytes are equal, False otherwise.
    """
    
    # hex representation to display messages
    ref_hex_byte = formater.from_int_to_hex(ref_byte)
    rd_hex_byte = formater.from_int_to_hex(rd_byte)
    
    if (ref_byte != rd_byte): # in case hex data differs
        if (storage == "reg"):
            error_msg.reg_cmp_mismatch(result_file_html, result_file_txt, ref_hex_byte, rd_hex_byte)
        elif (storage == "mem"):
            error_msg.mem_cmp_mismatch(result_file_html, result_file_txt, ref_hex_byte, rd_hex_byte)
        return False
    else :
        if (storage == "reg"):
            valid_msg.reg_cmp_match(result_file_html, result_file_txt, ref_hex_byte, rd_hex_byte)
        elif (storage == "mem"):
            valid_msg.mem_cmp_match(result_file_html, result_file_txt, ref_hex_byte, rd_hex_byte)
        return True


def rd_spi_transaction(
    spi_handler: nb_pkg.SPI_Object,
    result_file_html: nb_pkg.TextIO,
    result_file_txt: nb_pkg.TextIO,
    command : str,
    spi_cmd : int,
    addr : list
) -> tuple[bool, list[int]]:
    """
    Performs a low-level SPI read transaction.

    Args:
        spi_handler: SPI interface object.
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): Command name.
        spi_cmd (int): SPI command code.
        addr (list): Address to read from.

    Returns:
        tuple: (valid_rd (bool), rd_line (list)) indicating if read was successful and the data read.
    """
    
    rd_line: list[int] = []
    data_number_token_to_read = nb_pkg.dict_data_number_token_to_read[command]
    
    # Send command to SPI
    spi.xfer(spi_handler, [spi_cmd]) # we don't get the first byte
    
    # Send address to SPI
    if (addr):
        for addr_token in addr:
            parsed_addr_token = formater.parse_packet(addr_token,"int")
            formated_addr = formater.format_token_field(nb_pkg.nb_bytes_per_token_addr, parsed_addr_token)
            spi.xfer(spi_handler, formated_addr) 
            
    transmitted_line_int = [spi_cmd] + formated_addr
    number_of_bytes, transmitted_line_joined = formater.format_sent_line(transmitted_line_int)
    status_msg.sending_msg(result_file_html, result_file_txt, command, transmitted_line_joined, number_of_bytes)
        
    # Waiting for command 
    valid_rd = wait_for_spi_cmd(spi_handler, spi_cmd) 

    # receive data 
    nb_bytes_to_get = data_number_token_to_read * nb_pkg.nb_bytes_per_token_data
    data_to_send = [0x00 for i in range(nb_bytes_to_get)]
    rd_line = spi.xfer(spi_handler, data_to_send) 
    rd_line.reverse()
        
    return valid_rd, rd_line 



def wr_spi_transaction(
    spi_handler: nb_pkg.SPI_Object,
    result_file_html: nb_pkg.TextIO,
    result_file_txt: nb_pkg.TextIO,
    command : str,
    spi_cmd : int,
    addr : list,
    data : list
) -> bool :        
    """
    Performs a low-level SPI write transaction.

    Args:
        spi_handler: SPI interface object.
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): Command name.
        spi_cmd (int): SPI command code.
        addr (list): Address to write to.
        data (list): Data to write.

    Returns:
        int: 1 if write was successful, 0 otherwise.
    """

    data_number_token_to_write = nb_pkg.dict_data_number_token_to_write[command]
    
    # Send command to SPI
    spi.xfer(spi_handler, [spi_cmd])


    # Send address to SPI
    if (addr):
        for addr_token in addr:
            parsed_addr_token = formater.parse_packet(addr_token,"int")
            formated_addr = formater.format_token_field(nb_pkg.nb_bytes_per_token_addr, parsed_addr_token)
            spi.xfer(spi_handler, formated_addr)   
        
    
    # Send data to SPI
    if (data):
        formated_data: list[int] = []
        for indice_token in range (data_number_token_to_write) : 
            token_to_send = data[indice_token]
            parsed_data_token = formater.parse_packet(token_to_send,"int")
            formated_token = formater.format_token_field(nb_pkg.nb_bytes_per_token_data, parsed_data_token)
            spi.xfer(spi_handler, formated_token)
            
            # Only for results 
            formated_data = formated_data + formated_token 
    
    transmitted_line_int = [spi_cmd] + formated_addr + formated_data
    number_of_bytes, transmitted_line_joined = formater.format_sent_line(transmitted_line_int)
    status_msg.sending_msg(result_file_html, result_file_txt, command, transmitted_line_joined, number_of_bytes)
        
    # Waiting for command 
    valid_wr = wait_for_spi_cmd(spi_handler, spi_cmd)        
    return valid_wr


def wait_for_spi_cmd(spi_handler: nb_pkg.SPI_Object, spi_cmd : int) -> bool:
    """
    Waits for a specific SPI command to be received.

    Args:
        spi_handler: SPI interface object.
        spi_cmd (int): SPI command code to wait for.

    Returns:
        bool: True if command received within max iterations, False otherwise.
    """
    
    # len_cmd = len(spi_cmd)
    nb_iterations = 0
    received_byte: int = 0
    cmd_received = False
    # print(f"searching for command {spi_cmd}")
    while ((received_byte != spi_cmd) and (nb_iterations < main_pkg.max_while_iterations)) :
        received_byte_list: list[int]= spi.xfer(spi_handler, [0x00])
        received_byte = received_byte_list[0]
        # if current_byte != 0:
        #     potential_cmd_byte = current_byte
        #     if len_cmd > 1 :
        #         data_to_send = [0x00 for i in range (len_cmd-1)]
        #         potential_cmd_byte = 
        #     cmd_hex = from_int_to_hex(current_byte)
        #     print(f"Current iteration is {nb_iterations} with byte {cmd_hex}")
        nb_iterations += 1
    if nb_iterations < main_pkg.max_while_iterations :
        cmd_received = True
    else :
        cmd_received = False
    return cmd_received


