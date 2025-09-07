## Author: Alexander Art

# Class for brush objects
class Brush:
    def __init__(self):
        # Set default brush settings
        self.shape = 'pixel'
        self.color = (255, 0, 255, 255)
        self.size = 5

    def set_brush_pixel(self):
        # Set brush shape to pixel (not affected by brush size)
        self.shape = 'pixel'

    def set_brush_brush(self):
        # Set brush shape to brush (circular, but softer than circle)
        self.shape = 'brush'

    def set_brush_circle(self):
        # Set brush shape to circle
        self.shape = 'circle'

    def increase_brush_size(self):
        self.size += 1

    def decrease_brush_size(self):
        self.size -= 1
        self.size = max(1, self.size)
    
    def get_brush_size_text(self):
        return str(self.size)
