## Author: Alexander Art

import pygame

from modules.ui.ui_style import Style

# Class for textbox UI elements
class Textbox:
    def __init__(self, rect, text, action=None, style=Style()):
        # This text's parent object. This gets set with parent.add_text(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and self.render() must be called explicitly.
        self.parent = None

        self.rect = pygame.Rect(rect) # Relative to parent
        
        # Displayed text
        self.text = text

        # Function to run with entered text
        self.action = action

        # Color and formatting of the textbox
        self.style = style

        # True if the mouse is hovering over the textbox and the textbox is not being covered by something else on a higher layer
        self.is_hovered = False

        # Time the textbox was clicked for rendering text cursor
        self.clicked_time = None

        # True if the text cursor is active in the textbox and is reading keyboard input
        self.active = False

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
        # Draw textbox bounding rect
        pygame.draw.rect(surface, self.style.textbox_bg_color, self.get_global_bounding_rect())

        # Render the text
        surface.blit(pygame.font.Font(None, self.style.textbox_text_size).render(self.text, True, self.style.textbox_text_color), (self.global_x + self.style.textbox_text_padding[0], self.global_y + self.style.textbox_text_padding[1]))

        # If the textbox is active, render the text cursor
        if self.active and (pygame.time.get_ticks() - self.clicked_time) % 1000 < 500:
            pygame.draw.rect(surface, self.style.textbox_cursor_color, (self.global_x + self.style.textbox_text_padding[0] + pygame.font.Font(None, self.style.textbox_text_size).size(self.text)[0], self.global_y + self.style.textbox_text_padding[1], self.style.textbox_cursor_width, pygame.font.Font(None, self.style.textbox_text_size).size(self.text)[1]))

    def mouse_over(self, hovered):
        # Runs every frame. Set self.is_hovered.
        # hovered is True only if the mouse is over this textbox and is not being blocked by a UI element on a higher layer.        
        self.is_hovered = hovered

    def left_mouse_down(self):
        # This function runs on the left mousedown event.
        
        # If this textbox was clicked and it has a parent, move it to the top layer of textboxes
        if self.is_hovered and self.parent is not None:
            self.parent.textboxes.remove(self)
            self.parent.textboxes.append(self)
    
        # If this textbox is pressed, make it active.
        if self.is_hovered:
            self.active = True
            self.clicked_time = pygame.time.get_ticks()

        # If this textbox is clicked out of, exit it and run its function.
        if not self.is_hovered and self.active:
            self.active = False
            self.action(self.text)

    def key_down(self, key, unicode):
        # This function runs on the keydown event when CTRL is not pressed.

        if self.active:
            if key == pygame.K_RETURN:
                # Exit textbox and run its function when enter is pressed
                self.active = False
                self.action(self.text)
            elif key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
                # Delete last character
                self.text = self.text[:-1]
            else:
                # Type from keyboard input
                self.text += unicode
