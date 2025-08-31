## Author: Alexander Art

import pygame

from modules.ui.ui_style import Style

# Class for button UI elements
class Button:
    def __init__(self, rect, action, label, style=Style()):
        # This button's parent object. This gets set with parent.add_button(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and rendering/input functions must be called explicitly.
        self.parent = None

        self.rect = pygame.Rect(rect) # Relative to parent
        self.action = action
        self.label = label

        # Color and formatting of the button
        self.style = style

        # True if the mouse is hovering over the button and the button is not being covered by something else on a higher layer
        self.is_hovered = False
        
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
        return self.rect

    def get_global_bounding_rect(self):
        return pygame.Rect(self.get_global_pos(), self.size)

    def render(self, surface):
        # Mouse position relative to the top left corner of the parent
        mouse_pos = (pygame.mouse.get_pos()[0] - self.parent.global_x, pygame.mouse.get_pos()[1] - self.parent.global_y)

        # Change the button color if it is being hovered
        if self.is_hovered:
            color = self.style.button_hovered_bg_color
        else:
            color = self.style.button_default_bg_color

        # Draw button bounding rect
        pygame.draw.rect(surface, color, self.get_global_bounding_rect())

        # Draw button label
        if self.is_hovered:
            surface.blit(pygame.font.Font(None, self.style.button_text_size).render(self.label, True, self.style.button_hovered_text_color), (self.global_x + self.style.button_text_padding[0], self.global_y + self.style.button_text_padding[1]))
        else:
            surface.blit(pygame.font.Font(None, self.style.button_text_size).render(self.label, True, self.style.button_default_text_color), (self.global_x + self.style.button_text_padding[0], self.global_y + self.style.button_text_padding[1]))

    def mouse_over(self, hovered):
        # Runs every frame. Set self.is_hovered.
        # hovered is True only if the mouse is over this button and is not being blocked by a UI element on a higher layer.        
        self.is_hovered = hovered

    def left_mouse_down(self):
        # This function runs on the left mousedown event.
        
        # If this button was clicked and it has a parent, move it to the top layer of buttons
        if self.is_hovered and self.parent is not None:
            self.parent.buttons.remove(self)
            self.parent.buttons.append(self)
    
        # If this button is pressed, run its function.
        if self.is_hovered:
            self.action()
