def write_html_msg(result_file_html, content : str) -> None :
    """
    Writes a message inside a <p> tag to the HTML result file.

    Args:
        result_file_html: File handle for HTML result output.
        content (str): Message content to write.
    """
    
    if (content == "" or content is None) :
        content = "No content given : "
        html_msg = start_p_html + content + end_p + "\n"
    else :
        html_msg = start_p_html + content + end_p + "\n"
    result_file_html.write(html_msg) 
    
def start_cmp_div() -> str :
    """
    Returns the opening HTML for a comparison section.

    Returns:
        str: HTML string for starting a comparison div.
    """
    
    content = f" <div class= \"compare\"> \n "
    content += f" <h2 class= \"compare\"> Comparison of read data and reference data : </h2> \n "
    return content 