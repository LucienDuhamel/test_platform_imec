"""
formater.ipynb

This module provides utility functions for converting between hexadecimal strings and integers representations,
as well as formatting and parsing data for SPI communication. It is used throughout the test platform to ensure consistent
data handling and conversion between formats required by hardware and test scripts.

Main functionalities:
    - Convert between hex strings, integers, and byte lists.
    - Format and parse command, address, and data fields for SPI transactions.
    - Provide helper functions for string/list conversions and data padding.

Intended usage:
    - Used by SPI command execution and parsing modules to prepare and interpret data.
    - Ensures correct byte order and padding for hardware compatibility.
"""

def from_hex_to_bit(hex_value : str) :
    """
    Converts a hexadecimal string to its 8-bit binary representation.

    Args:
        hex_value (str): Hexadecimal string (e.g., 'A3').

    Returns:
        str: 8-bit binary string (e.g., '10100011').

    Example:
        >>> from_hex_to_bit('A3')
        '10100011'
    """
    return '{0:08b}'.format(int(hex_value, 16))

def from_hex_to_int(hex_value : str) -> int :
    """
    Converts a hexadecimal string to an integer.

    Args:
        hex_value (str): Hexadecimal string (e.g., '1F').

    Returns:
        int: Integer value.

    Example:
        >>> from_hex_to_int('1F')
        31
    """
    return int(hex_value, 16)

def from_list_hex_to_int(hex_list : list) -> list :
    """
    Converts a list of hexadecimal strings to a list of integers.

    Args:
        hex_list (list): List of hex strings (e.g., ['1A', 'FF']).

    Returns:
        list: List of integers (e.g., [26, 255]).

    Example:
        >>> from_list_hex_to_int(['1A', 'FF'])
        [26, 255]
    """
    nb_byte_from_list = len(hex_list)
    list_int_bytes = []
    for byte_indice in range (nb_byte_from_list) : 
        int_byte = from_hex_to_int(hex_list[byte_indice])
        list_int_bytes.append(int_byte)
    return list_int_bytes


def from_int_to_hex(int_val : int) -> str :
    """
    Converts an integer to a two-character uppercase hexadecimal string.

    Args:
        int_val (int): Integer value (e.g., 31).

    Returns:
        str: Hexadecimal string (e.g., '1F').

    Example:
        >>> from_int_to_hex(31)
        '1F'
    """
    
    hex_val = '{0:02x}'.format(int_val)
    return hex_val.upper()


def from_list_int_to_hex(int_list : list) -> list :
    """
    Converts a list of integers to a list of two-character uppercase hexadecimal strings.

    Args:
        int_list (list): List of integers (e.g., [31, 255]).

    Returns:
        list: List of hex strings (e.g., ['1F', 'FF']).

    Example:
        >>> from_list_int_to_hex([31, 255])
        ['1F', 'FF']
    """
    
    nb_byte_from_list = len(int_list)
    list_hex_bytes = []
    for byte_indice in range (nb_byte_from_list) : 
        hex_byte = from_int_to_hex(int_list[byte_indice])
        list_hex_bytes.append(hex_byte.upper())
    return list_hex_bytes

def list_to_string (List : list) -> str:
    """
    Concatenates a list of strings into a single string.

    Args:
        List (list): List of strings (e.g., ['1F', 'FF']).

    Returns:
        str: Concatenated string (e.g., '1FFF').

    Example:
        >>> list_to_string(['1F', 'FF'])
        '1FFF'
    """
    
    string = ''
    for element in List :
        string += element
    return string
    
# Take a string composed of hex val (no spaces) and parses it into nb_hex_per_packet hex packets
def make_hex_packets(data : str, nb_hex_per_packet : int) -> str:
    """
    Splits a string of hex values into packets of fixed length.

    Args:
        data (str): Hex string (e.g., '1234ABCD').
        nb_hex_per_packet (int): Number of hex characters per packet.

    Returns:
        str: Concatenated packets (e.g., '1234ABCD' with 4 -> '1234ABCD').

    Example:
        >>> make_hex_packets('1FFF163256789ABC', 8)
        '1FFF1632 56789ABC '
    """
    
    length_data = len(data)
    parsed_data = ''
    for i in range(0,length_data,nb_hex_per_packet):
        parsed_data += data[i:i+nb_hex_per_packet]+' '
    return parsed_data


# Take the 8 hex values and transforms it into list of 2 hex packets
def parse_packet (data : str, mode : str) -> list :
    """
    Parses a hex string into a list of bytes, either as strings or integers.

    Args:
        data (str): Hex string (e.g., '1F2A').
        mode (str): 'str' for string output, 'int' for integer output.

    Returns:
        list: List of bytes as strings or integers.

    Raises:
        Exception: If mode is not 'str' or 'int'.

    Example:
        >>> parse_packet('1F2A', 'str')
        ['1F', '2A']
        >>> parse_packet('1F2A', 'int')
        [31, 42]
    """
    
    bytes_list : list[str|int]= []
    if (len(data)%2 == 1):
        data = '0' + data  
    for i in range(0, len(data), 2) :
        hex_str = data[i:i+2]
        if (mode == 'str'):
            bytes_list.append(hex_str)
        elif (mode == "int"):
            hex_str = '0x' + hex_str
            bytes_list.append(int(hex_str, 16))
        else :
            message = "wrong mode passed in argument"
            raise Exception(message)
    return bytes_list

def parse_list_of_packets(list_of_packets : list, mode : str) -> list:
    """
    Parses a list of hex strings into a flat list of bytes, as strings or integers.

    Args:
        list_of_packets (list): List of hex strings (e.g., ['1F2A', '00FF']).
        mode (str): 'str' or 'int'.

    Returns:
        list: Flattened list of bytes.

    Example:
        >>> parse_list_of_packets(['1FFF1632', '56789ABC'], 'int')
        [31, 255, 22, 50, 86, 120, 154, 188]
    """
    
    parsed_list: list=[]
    for packet in list_of_packets :
        parsed_list = parsed_list + parse_packet(packet,mode)
    return parsed_list



def format_token_field (ref_byte_length : int, field_data : list) -> list:
    """
    Pads a list of bytes with zeros on the left to match the required length, then reverses for LSB-first order.

    Args:
        ref_byte_length (int): Required length of the field.
        field_data (list): List of bytes (as ints).

    Returns:
        list: Padded and reversed list.

    Example:
        >>> format_token_field(2, [0x20])
        [32, 0]
    """
    
    nb_bytes = len(field_data)
    while nb_bytes < ref_byte_length :
        field_data = [0] + field_data # add 0 bytes to the left until we match the correct size
        nb_bytes += 1
    field_data.reverse() # send from LSB to MSB
    return field_data

# Implements the basic behaviour of the read commands
def format_rd_data (rd_line : list, nb_hex_per_packet : int) :
    """
    Formats a list of read bytes into a string of hex packets.

    Args:
        rd_line (list): List of bytes (as ints).
        nb_hex_per_packet (int): Number of hex characters per packet.

    Returns:
        str: Formatted string of hex packets.

    Example:
        >>> format_rd_data([31, 255, 22, 50, 86, 120, 154, 188], 8)
        '1FFF1632 56789ABC '
    """
    
    rd_line_hex_bytes = from_list_int_to_hex(rd_line)
    rd_line_str = list_to_string(rd_line_hex_bytes)
    formated_rd_line = make_hex_packets(rd_line_str, nb_hex_per_packet)

    return formated_rd_line



def from_list_to_str(L : list):
    """
    Converts a list of elements to a single space-separated string.

    Args:
        L (list): List of elements.

    Returns:
        str: Space-separated string of elements.
    """
    
    content = ""
    for element in L :
        content += str(element) + " "
    return content

import doctest
doctest.testmod()

# def format_cmp_data(data, mode):
#     int_list = parse_list_of_packets(data, "int")
#     return int_list


# data = ["01234567", "76543210"]
# L = format_cmp_data(data, "int")
# print(L)
# print(type(L[0]))


def format_parsed_line(parsed_line : list) -> str:
    """
    Formats a parsed command line into a string.

    Args:
        parsed_line (list): Parsed command line.

    Returns:
        str: Formatted command line string.
    """
    
    command = parsed_line[0]
    line = [command]
    for token_field in parsed_line[1::] :
        if (token_field):
            line.append(token_field)
    return from_list_to_str(line)


def format_sent_line(sent_line : list) -> tuple[int, str]:
    """
    Formats a sent command line into a string.

    Args:
        sent_line (list): Sent command line.

    Returns:
        str: Formatted command line string.
    """
    
    transmitted_line_hex = from_list_int_to_hex(sent_line)
    number_of_bytes = len(transmitted_line_hex) 
    transmitted_line_joined = from_list_to_str(transmitted_line_hex)
    return number_of_bytes, transmitted_line_joined