"""
    This module provides functions to initialize and finalize HTML and TXT result files for test reports.
    It includes functions to write headers, footers, and formatted content into these files.        
    The HTML files are styled with CSS for better readability, while TXT files are plain text.
    Intended usage:
        - Used by test scripts to log results in a structured format.
        - Facilitates easy viewing of test results in both HTML and TXT formats.
"""
from .reports_pkg import text_colors, highlight_colors



# Function which launch a test and writes in an html result file 
def init_html_result_file(test_file_name, test_file_path, css_file):
    """
    Initializes and opens an HTML result file for writing test results.

    Args:
        test_file_name (str): Name of the test file.
        test_file_path (str): Path to the test file.
        css_file (str): CSS style content to include in the HTML.

    Returns:
        file object: Opened HTML file handle.
    """
    
    result_file_path_html = "out/" + test_file_name + '_results.html'
    result_file_html = open(result_file_path_html,"w")
    result_file_html_title = "Output Data in an HTML file"
    header_content = f'Results from {test_file_name}'
    html_content = initiate_html_content(result_file_html_title, css_file, header_content)
    result_file_html.write(html_content)
    return result_file_html

def end_html_result_file(result_file_html) -> None:
    """
    Writes the HTML footer and closes the HTML result file.
    """
    
    result_file_html.write(end_html())
    result_file_html.close()



def initiate_html_content(title : str, style_css : str, main_header_content : str) -> str :
    """
    Generates the initial HTML content for the result file, including headers and styles.

    Args:
        title (str): Title of the HTML document.
        style_css (str): CSS styles to include.
        main_header_content (str): Main header text for the HTML body.

    Returns:
        str: HTML content as a string.
    """
    
    content = f"<!DOCTYPE html> \n "
    content += f"<html>\n<head> \n \
    <title>{title}</title> \n \
    <style>  {style_css} </style> \n \
    </head> \n <body> \n \
    <div class = \"main\"> \n "

    content += f"<h1> {main_header_content} </h1> \n"
    return content 


def end_html() -> str :
    """
    Returns the closing HTML tags for the result file.

    Returns:
        str: HTML string for ending the document.
    """
    
    return "</body> \n </html>"

def start_cmp_div() -> str :
    """
    Returns the opening HTML for a comparison section.

    Returns:
        str: HTML string for starting a comparison div.
    """
    
    content = f" <div class= \"compare\"> \n "
    content += f" <h2 class= \"compare\"> Comparison of read data and reference data : </h2> \n "
    return content 


def end_cmp_div() -> str :
    """
    Returns the closing HTML for a comparison section.

    Returns:
        str: HTML string for ending a comparison div.
    """
    
    return " </div> \n "


def start_p_html() -> str :
    """
    Returns the opening HTML for a paragraph.

    Returns:
        str: HTML string for starting a paragraph.
    """

    return f"<p style=\"color:{text_colors['default_color']};\">"

def end_p_html() -> str :
    """
    Returns the closing HTML for a paragraph.

    Returns:
        str: HTML string for ending a paragraph.
    """
    
    return "</p>"


def start_error_span() -> str :
    """
    Returns the opening HTML for an error message span.

    Returns:
        str: HTML string for starting an error span.
    """
    
    return f"<span style=\"color:{text_colors['error_color']};  background-color: {highlight_colors['error_color']};\">"


def start_valid_span() -> str :
    """
    Returns the opening HTML for a validation message span.

    Returns:
        str: HTML string for starting a validation span.
    """
    
    return f"<span style=\"color:{text_colors['validation_color']}; background-color: {highlight_colors['validation_color']};\">"



def end_span() -> str :
    """
    Returns the closing HTML for a span.

    Returns:
        str: HTML string for ending a span.
    """
    
    return "</span>"


def write_html_msg(result_file_html, content : str) -> None :
    """
    Writes a message inside a <p> tag to the HTML result file.

    Args:
        result_file_html: File handle for HTML result output.
        content (str): Message content to write.
    """
    
    if (content == "" or content is None) :
        content = "No content given : "
        html_msg = start_p_html() + content + end_p_html() + "\n"
    else :
        html_msg = start_p_html() + content + end_p_html() + "\n"
    result_file_html.write(html_msg) 


def error_msg_html() -> str :
    """
    Returns the HTML formatted error message.

    Returns:
        str: HTML string for an error message.
    """
    
    return f"{start_error_span()} ERROR : {end_span()}"

def valid_msg_html() -> str :
    """
    Returns the HTML formatted validation message.

    Returns:
        str: HTML string for a validation message.
    """
    
    return f"{start_valid_span()} SUCCESSFUL : {end_span()}"