# mypackage/config.py
from ..functions import load_config

file_name = "style_config.yaml"
style_cfg = load_config(file_name)

text_colors = style_cfg["html_config"]["text_colors"]
highlight_colors = style_cfg["html_config"]["highlight_colors"]

red_color = style_cfg["print_msg"]["red_color"]
green_color = style_cfg["print_msg"]["green_color"]
normal_color = style_cfg["print_msg"]["normal_color"]



    
