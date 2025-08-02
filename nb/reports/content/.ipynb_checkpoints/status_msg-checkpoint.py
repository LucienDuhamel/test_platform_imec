def executing_line_msg(result_file_html, result_file_txt, command : str, parsed_line : list) -> None :
    """
    Logs the execution of a command line.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): Command name.
        parsed_line (list): Parsed command line.
    """
    
    command = parsed_line[0]
    line = [command]
    for token_field in parsed_line[1::] :
        if (token_field):
            line = line + token_field
    line_joined = from_list_to_str(line)
    message = f"{command} \t {line_joined}  \n " 
    if (activate_msg_prints):
        print(message)
    if (activate_result_file_txt):
        result_file_txt.write(message)
    if (activate_result_file_html):
        write_html_msg(result_file_html, message)


def sending_msg (result_file_html, result_file_txt, command : str, line : list) -> None :
    """
    Logs the sending of a command and its data.

    Args:
        result_file_html: File handle for HTML result output.
        result_file_txt: File handle for TXT result output.
        command (str): Command name.
        line (list): Data sent.
    """
    
    number_of_bytes = len(line) 
    line_joined = from_list_to_str(line)
    message = f"{command} ({number_of_bytes}) : {line_joined} \n "
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