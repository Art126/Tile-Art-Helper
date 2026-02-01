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

    def set_brush_size(self, size):
        try:
            if int(size) > 0:
                self.size = int(size)
        except ValueError:
            pass

    def increase_brush_size(self):
        self.size += 1

    def decrease_brush_size(self):
        self.size -= 1
        self.size = max(1, self.size)
    
    def get_brush_size_text(self):
        return str(self.size)

    def set_red(self, red):
        try:
            if 0 <= int(red) <= 255:
                self.color = (int(red), self.color[1], self.color[2], self.color[3])
        except ValueError:
            pass

    def set_green(self, green):
        try:
            if 0 <= int(green) <= 255:
                self.color = (self.color[0], int(green), self.color[2], self.color[3])
        except ValueError:
            pass

    def set_blue(self, blue):
        try:
            if 0 <= int(blue) <= 255:
                self.color = (self.color[0], self.color[1], int(blue), self.color[3])
        except ValueError:
            pass

    def set_alpha(self, alpha):
        try:
            if 0 <= int(alpha) <= 255:
                self.color = (self.color[0], self.color[1], self.color[2], int(alpha))
        except ValueError:
            pass
