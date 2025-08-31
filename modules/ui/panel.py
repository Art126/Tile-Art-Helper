## Author: Alexander Art

import pygame

from modules.ui.ui_style import Style
from modules.ui.button import Button

# Class for panel UIs
class Panel:
    def __init__(self, rect, fixed, style=Style()):
        # This panel's parent object. This gets set with parent.add_panel(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and rendering/input functions must be called explicitly.
        self.parent = None
        
        # Create rect object from rect argument.
        # Rect left (x) and top (y) values become the local x and y values for the panel.
        self.rect = pygame.Rect(rect)

        # True if the panel should be fixed and not have a title bar.
        # False if the panel should have a title bar, be movable, and be closable.
        self.fixed = fixed

        # Color and formatting of the panel
        self.style = style

        # True when the panel is open
        # False when the panel is closed
        self.visible = True

        # True if the mouse is hovering over the panel and the panel is not being covered by something else on a higher layer
        self.is_hovered = False

        # Can be set with .set_caption()
        self.title = ""

        # If the panel is movable, this keeps track of when it is being moved.
        self.title_bar_held = False

        # Panels, canvases, buttons, and text may be added as child objects.
        self.panels = []
        self.canvases = [] # Needing several canvases is rare.
        self.buttons = []
        self.sliders = []
        self.text = []

        if self.fixed:
            self.close_button = None
        else:
            self.close_button = Button((self.width - self.style.panel_title_bar_height, -self.style.panel_title_bar_height, self.style.panel_title_bar_height, self.style.panel_title_bar_height),
                                       self.toggle_visibility,
                                       "x",
                                       Style(button_default_bg_color=(255, 255, 255), button_hovered_bg_color=(255, 0, 0), button_default_text_color=(0, 0, 0), button_hovered_text_color=(255, 255, 255), button_text_size=self.style.panel_title_bar_text_size, button_text_padding=(5, 2)))
            self.add_button(self.close_button)

    @property
    def size(self):
        return self.rect.size

    @size.setter
    def size(self, value):
        self.rect.size = value

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, value):
        self.rect.width = value

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, value):
        self.rect.height = value
        
    @property
    def local_x(self):
        return self.rect.x

    @local_x.setter
    def local_x(self, value):
        self.rect.x = value

    @property
    def local_y(self):
        return self.rect.y

    @local_y.setter
    def local_y(self, value):
        self.rect.y = value

    def get_local_pos(self):
        return (self.local_x, self.local_y)

    def get_global_pos(self):
        if self.parent is not None:
            parent_pos = self.parent.get_global_pos() # Avoids redundant recursive calls
            return (parent_pos[0] + self.local_x, parent_pos[1] + self.local_y)
        else:
            return (self.local_x, self.local_y)

    @property
    def global_x(self):
        return self.get_global_pos()[0]

    @property
    def global_y(self):
        return self.get_global_pos()[1]

    def get_local_bounding_rect(self):
        if self.fixed:
            return self.rect
        else:
            return pygame.Rect(self.local_x, self.local_y - self.style.panel_title_bar_height, self.width, self.height + self.style.panel_title_bar_height)

    def get_global_bounding_rect(self):
        if self.fixed:
            return pygame.Rect(self.get_global_pos(), self.size)
        else:
            return pygame.Rect(self.global_x, self.global_y - self.style.panel_title_bar_height, self.width, self.height + self.style.panel_title_bar_height)

    def get_local_title_bar_rect(self):
        if self.fixed:
            return None
        else:
            return pygame.Rect(self.local_x, self.local_y - self.style.panel_title_bar_height, self.width, self.style.panel_title_bar_height)

    def get_global_title_bar_rect(self):
        if self.fixed:
            return None
        else:
            return pygame.Rect(self.global_x, self.global_y - self.style.panel_title_bar_height, self.width, self.style.panel_title_bar_height)

    def set_caption(self, caption):
        self.title = caption
        return self
            
    def add_panel(self, panel):
        self.panels.append(panel)
        panel.parent = self
        return self

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.parent = self
        return self

    def add_button(self, button):
        self.buttons.append(button)
        button.parent = self
        return self

    def add_slider(self, slider):
        self.sliders.append(slider)
        slider.parent = self
        return self

    def add_text(self, text):
        self.text.append(text)
        text.parent = self
        return self

    def keep_on_screen(self):
        if not self.fixed:
            self.local_x = max(self.local_x, 0)
            self.local_x = min(self.local_x, self.parent.width - self.width)
            self.local_y = max(self.local_y, self.style.panel_title_bar_height)
            self.local_y = min(self.local_y, self.parent.height)

    def toggle_visibility(self):
        if self.visible:
            self.parent.panels.remove(self)
            self.visible = False
            # Update every child element
            for panel in self.panels:
                panel.mouse_over(False)
                panel.visible = False
            for button in self.buttons:
                button.mouse_over(False)
            for slider in self.sliders:
                slider.mouse_over(False)
            for canvas in self.canvases:
                canvas.mouse_over(False)
        else:
            self.parent.add_panel(self)
            self.visible = True

    def render(self, surface):
        # Render the panel rect onto the passed surface.
        pygame.draw.rect(surface, self.style.panel_bg_color, self.get_global_bounding_rect())
        
        # If this panel is not fixed, draw the title bar and its caption onto the passed surface.
        if not self.fixed:
            pygame.draw.rect(surface, self.style.panel_title_bar_color, self.get_global_title_bar_rect())
            surface.blit(pygame.font.Font(None, self.style.panel_title_bar_text_size).render(self.title, True, self.style.panel_title_bar_text_color), (self.global_x + 3, self.global_y - self.style.panel_title_bar_height + 2))

        # Note that there is an inconsistency in the order of how the children are rendered:
        # Child panels are rendered below child buttons, but child panels can cover child buttons from being pressed.
        # There are no cases yet where a panel has both child panels and child buttons, so it has not yet been decided which should be on top.

        # Render child canvases
        for canvas in self.canvases:
            canvas.render(surface)

        # Render child panels
        for panel in self.panels:
            panel.render(surface)

        # Render child buttons
        for button in self.buttons:
            button.render(surface)

        # Render child sliders
        for slider in self.sliders:
            slider.render(surface)
            
        # Render child text
        for text in self.text:
            text.render(surface)

    def mouse_over(self, hovered):
        # Runs every frame. Set self.is_hovered and calculate which child elements are being hovered by the mouse.
        # hovered is True only if the mouse is over this panel and is not being blocked by a UI element on a higher layer.
        # If self.is_hovered is False, then all children will also have is_hovered set to False.
        
        self.is_hovered = hovered

        # Pass mouse hover to only the top UI element that the mouse is over
        # Layer order, sequentially up the list of each: panels, buttons, sliders, canvases
        element_found = False
        for index, panel in enumerate(reversed(self.panels)):
            if self.is_hovered and panel.get_global_bounding_rect().collidepoint(pygame.mouse.get_pos()) and not element_found:
                panel.mouse_over(True)
                element_found = True
            else:
                panel.mouse_over(False)
        for index, button in enumerate(reversed(self.buttons)):
            if self.is_hovered and button.get_global_bounding_rect().collidepoint(pygame.mouse.get_pos()) and not element_found:
                button.mouse_over(True)
                element_found = True
            else:
                button.mouse_over(False)
        for index, slider in enumerate(reversed(self.sliders)):
            if self.is_hovered and slider.get_global_bounding_rect().collidepoint(pygame.mouse.get_pos()) and not element_found:
                slider.mouse_over(True)
                element_found = True
            else:
                slider.mouse_over(False)
        for index, canvas in enumerate(reversed(self.canvases)):
            if self.is_hovered and canvas.get_global_bounding_rect().collidepoint(pygame.mouse.get_pos()) and not element_found:
                canvas.mouse_over(True)
                element_found = True
            else:
                canvas.mouse_over(False)

    def mouse_moved(self, mouse_rel):
        # This function runs every frame the mouse moves.

        # If the panel is being dragged, make it follow the mouse
        if self.title_bar_held:
            self.local_x += mouse_rel[0]
            self.local_y += mouse_rel[1]

        # Pass mouse move to child panels
        for panel in self.panels:
            panel.mouse_moved(mouse_rel)

        # Pass mouse move to child canvases
        for canvas in self.canvases:
            # The mouse move does not need to be passed to the canvases if the mouse did not move
            if not (mouse_rel[0] == 0 and mouse_rel[1] == 0):
                canvas.mouse_moved(mouse_rel)

        # Pass mouse move to child sliders
        for slider in self.sliders:
            # The mouse move does not need to be passed to the sliders if the mouse did not move
            if not (mouse_rel[0] == 0 and mouse_rel[1] == 0):
                slider.mouse_moved(mouse_rel)

    def left_mouse_down(self):
        # This function runs on the left mousedown event.

        # If this panel was clicked, has a parent, and is not fixed, then move it to the top layer of panels
        if self.is_hovered and self.parent is not None and not self.fixed:
            self.parent.panels.remove(self)
            self.parent.panels.append(self)
            
        if not self.fixed:
            # If it was not pressed, then detect when the title bar is pressed
            if self.is_hovered and self.get_global_title_bar_rect().collidepoint(pygame.mouse.get_pos()):
                self.title_bar_held = True

        # Pass mouse press to child panels
        for panel in self.panels[:]:
            panel.left_mouse_down()

        # Pass mouse press to child canvases
        for canvas in self.canvases[:]:
            canvas.left_mouse_down()

        # Pass mouse press to child buttons
        for button in self.buttons[:]:
            button.left_mouse_down()

        # Pass mouse press to child sliders
        for slider in self.sliders[:]:
            slider.left_mouse_down()

    def left_mouse_up(self):
        # This function runs on the left mouseup event.
        
        self.title_bar_held = False

        # To keep the title bar visible, ensure that the title bar is not dragged off the parent panel
        self.keep_on_screen()

        # Pass mouse up to child panels
        for panel in self.panels:
            panel.left_mouse_up()

        # Pass mouse up to child canvases
        for canvas in self.canvases:
            canvas.left_mouse_up()

        # Pass mouse up to child sliders
        for slider in self.sliders:
            slider.left_mouse_up()
