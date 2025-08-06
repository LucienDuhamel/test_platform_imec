"""
translator.ipynb

This module provides a set of functions to parse, execute, and validate SPI (Serial Peripheral Interface) commands for a test platform.
It supports reading and writing to registers and memory, as well as comparing read data against reference values using masks.
The results of each operation are logged to both HTML and TXT result files for reporting and debugging purposes.

Main functionalities:
    - Execute SPI commands parsed from a test file (REGRD, REGWR, MEMRD, MEMWR, MEMRDM, MEMWRM, REGCMP, MEMCMP).
    - Perform SPI read and write transactions.
    - Compare register and memory data with reference values and masks.
    - Log all actions and results in a human-readable format.

Intended usage:
    - Used as part of an automated test platform for SPI devices.
    - Functions are designed to be called with parsed command lines and maintain state between operations.

Dependencies:
    - Assumes existence of SPI interface object (AxiQspi) and several helper functions for formatting, parsing, and messaging.
    - Relies on global configuration variables for command codes and data formatting.

Author: [Lucien Duhamel]
Date: [2025-07-29]
"""
from .nb_pkg import commands, TextIO
from .reports.content.error_msg import unknown_cmd

def parse_file(test_file: TextIO, result_file_html: TextIO, result_file_txt: TextIO) -> dict : 
    """
    Parses a test file containing SPI commands and organizes them into a dictionary.

    Each line is split into command, address, and data fields based on the command dictionary (see commands.yaml).
    Comments (lines starting with '//') are ignored. Unknown commands are logged.

    Args:
        test_file: An iterable file object containing the test commands.
        result_file_html: File handle for HTML result output (for logging unknown commands).
        result_file_txt: File handle for TXT result output (for logging unknown commands).

    Returns:
        dict: Dictionary mapping command indices to parsed command lines (command, address, data).
        
    Note:
        The command dictionary (cmd_dict) is directly shaped in respect with the commands.yaml file.
    """

    nb_cmd = 0
    parsed_file : dict[int, list] = {} # dictionnary composed of all command lines from test file.
    parsed_line = [] # one parsed line from the test file : command, addr, bytes in this exact order

    # Open and read the file
    for line in test_file:
        line = line.strip()  # Remove extra spaces and newline characters
        if line.startswith("//"): # Ignore comments 
            continue
        parts = line.split() # Split the line into a list of string based on spaces
        if (parts) :
            command = parts[0]
            if command in commands :
                nb_cmd += 1
                tokens = commands[command]["tokens"]
                addr, data = extract_tokens(parts, tokens)
                parsed_line = [command, addr, data]
                parsed_file[nb_cmd]=parsed_line
            else:
                unknown_cmd(result_file_html, result_file_txt, command)
    return parsed_file


def extract_tokens(parts : list, tokens: dict):
    """
    Extracts address and data tokens from a split command line.

    Args:
        parts (list): List of strings representing the split command line.
        tokens (dict): Dictionary specifying the number of address and data tokens.

    Returns:
        tuple: (addr, data) where addr and data are lists of strings or None if not present.
    """
    
    if ("addr" in tokens) :
        addr_token_length = tokens["addr"]
        addr = parts[1:1+addr_token_length]
    else :
        addr = None
    if ("data" in tokens):
        data_tokens_length = tokens["data"]
        if(addr):
            data = parts[1+addr_token_length:1+addr_token_length+data_tokens_length]
        else :
            data = parts[1:1+data_tokens_length]
    else :
        data = None
    return addr, data
