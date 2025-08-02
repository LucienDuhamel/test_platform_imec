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

def end_html_result_file() -> None:
    """
    Writes the HTML footer and closes the HTML result file.
    """
    
    result_file_html.write(end_html())
    result_file_html.close()


def init_txt_result_file(test_file_name, test_file_path):
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

def end_txt_result_file() -> None:
    """
    Writes the TXT footer and closes the TXT result file.
    """
    
    end_txt_file = "End of results for this file"
    result_file_txt.write(end_txt_file)
    result_file_txt.close()


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
    
    return "</div> \n </body> \n </html>"