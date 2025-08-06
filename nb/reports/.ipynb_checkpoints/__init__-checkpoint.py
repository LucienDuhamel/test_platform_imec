from . import content  # Import the messages package for direct access

from .builder_html import (
    init_html_result_file,
    end_html_result_file,
    initiate_html_content,
)

from .builder_txt import (
    init_txt_result_file,
    end_txt_result_file,
)


__all__ = [
    "content",
    
    "init_html_result_file",
    "end_html_result_file",
    "initiate_html_content",
    
    "init_txt_result_file",
    "end_txt_result_file",
]