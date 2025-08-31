## Author: Alexander Art

# Class for UI element styles
class Style:
    def __init__(self,
                 panel_bg_color=(127, 63, 0),
                 panel_title_bar_color=(255, 255, 255),
                 panel_title_bar_text_color=(0, 0, 0),
                 panel_title_bar_text_size=24,
                 panel_title_bar_height=20,
                 button_default_bg_color=(63, 0, 0),
                 button_hovered_bg_color=(255, 127, 63),
                 button_default_text_color=(255, 255, 255),
                 button_hovered_text_color=(255, 255, 255),
                 button_text_size=32,
                 button_text_padding=(9, 9)):
        self.panel_bg_color = panel_bg_color
        self.panel_title_bar_color = panel_title_bar_color
        self.panel_title_bar_text_color = panel_title_bar_text_color
        self.panel_title_bar_text_size = panel_title_bar_text_size
        self.panel_title_bar_height = panel_title_bar_height
        self.button_default_bg_color = button_default_bg_color
        self.button_hovered_bg_color = button_hovered_bg_color
        self.button_default_text_color = button_default_text_color
        self.button_hovered_text_color = button_hovered_text_color
        self.button_text_size = button_text_size
        self.button_text_padding = button_text_padding
