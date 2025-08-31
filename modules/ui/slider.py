## Author: Alexander Art

import pygame

# Class for slider UI elements
class Slider:
    def __init__(self, pos, min_value, max_value, color=(0, 0, 0)):
        # This slider's parent object. This gets set with parent.add_slider(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and self.render() must be called explicitly.
        self.parent = None

        self.pos = pos
        self.min_value = min_value
        self.max_value = max_value
        self.color = color

        self.percentage = 0

        self.is_hovered = False
        self.is_held = False

    @property
    def size(self):
        return (12, self.height)

    @property
    def width(self):
        return 12

    @property
    def height(self):
        return 60
        
    @property
    def local_x(self):
        return self.pos[0]

    @local_x.setter
    def local_x(self, value):
        self.pos = (value, self.pos[1])

    @property
    def local_y(self):
        return self.pos[1]

    @local_y.setter
    def local_y(self, value):
        self.pos = (self.pos[0], value)

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
        return pygame.Rect(self.get_local_pos(), self.size)

    def get_global_bounding_rect(self):
        return pygame.Rect(self.get_global_pos(), self.size)

    def get_value(self):
        return self.min_value + self.percentage * (self.max_value - self.min_value)

    def render(self, surface):
        # Draw the filled in part
        pygame.draw.rect(surface, self.color, (self.global_x + 3, self.global_y, 6, self.height))
        # Draw the not filled in part
        pygame.draw.rect(surface, (0, 0, 0), (self.global_x + 3, self.global_y, 6, (1 - self.percentage) * self.height))
        # Draw the draggable part
        pygame.draw.rect(surface, (255, 255, 255), (self.global_x, self.global_y + (1 - self.percentage) * (self.height - 6), self.width, 6))

    def mouse_over(self, hovered):
        # Runs every frame. Set self.is_hovered.
        # hovered is True only if the mouse is over this slider and is not being blocked by a UI element on a higher layer.        
        self.is_hovered = hovered

    def mouse_moved(self, mouse_rel):
        # Mouse position relative to the top left corner of the slider
        mouse_pos = (pygame.mouse.get_pos()[0] - self.global_x, pygame.mouse.get_pos()[1] - self.global_y)
        
        if self.is_held:
            self.percentage = min(max(0, 1 - (mouse_pos[1] - 3) / (self.height - 6)), 1)

    def left_mouse_down(self):
        # If the slider was clicked
        if self.is_hovered:
            # If this slider has a parent, move it to the top layer of sliders
            if self.parent is not None:
                self.parent.sliders.remove(self)
                self.parent.sliders.append(self)
            
            self.is_held = True

            # Mouse position relative to the top left corner of the slider
            mouse_pos = (pygame.mouse.get_pos()[0] - self.global_x, pygame.mouse.get_pos()[1] - self.global_y)
            
            self.percentage = min(max(0, 1 - (mouse_pos[1] - 3) / (self.height - 6)), 1)

    def left_mouse_up(self):
        self.is_held = False
