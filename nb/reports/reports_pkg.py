# mypackage/config.py
from ..functions import load_config


style_cfg = load_config("style_config.yaml")

text_colors = style_cfg["html_config"]["text_colors"]
highlight_colors = style_cfg["html_config"]["highlight_colors"]

red_color = style_cfg["print_msg"]["red_color"]
green_colour = style_cfg["print_msg"]["green_color"]


    
