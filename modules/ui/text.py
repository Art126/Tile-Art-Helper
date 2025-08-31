## Author: Alexander Art

import pygame

# Class for text UI elements
class Text:
    def __init__(self, message, size, color, pos):
        # This text's parent object. This gets set with parent.add_text(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and self.render() must be called explicitly.
        self.parent = None
        
        # Text string
        self.message = message

        # Font size
        self.size = size

        # Font color
        self.color = color

        # Text position (relative to the surface or parent panel that the text is rendered on)
        self.local_x = pos[0]
        self.local_y = pos[1]

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

    def render(self, surface):
        # If the string is given by a function, then call the function.
        if callable(self.message):
            message = self.message()
        else:
            message = self.message

        # Render the text
        surface.blit(pygame.font.Font(None, self.size).render(message, True, self.color), self.get_global_pos())
