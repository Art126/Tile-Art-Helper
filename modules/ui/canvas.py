## Author: Alexander Art

import math
from tkinter import filedialog

import pygame

import modules.utils

# Class for canvas UI element
class Canvas:
    def __init__(self, rect, brush):
        # This canvas's parent object. This gets set with parent.add_canvas(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and rendering/input functions must be called explicitly.
        self.parent = None

        # Create rect object from rect argument.
        # Rect left (x) and top (y) values become the local x and y values for the canvas.
        self.rect = pygame.Rect(rect)

        # Brush object for this canvas to read brush settings from
        self.brush = brush

        # True if the mouse is hovering over the canvas and the canvas is not being covered by something else on a higher layer
        self.is_hovered = False

        self.zoom = 1 # zoom < 1 means zoomed out. zoom > 1 means zoomed in.
        self.scroll = [0, 0]

        self.loaded_image = None
        self.open_filepath = None
        self.image_loaded = False

        # True when the brush is being painted on the canvas.
        self.brush_down = False

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

    def get_coords_text(self):
        # Returns the coordinates of the mouse position on the canvas as text.

        # Mouse position relative to the top left corner of the canvas
        mouse_pos = (pygame.mouse.get_pos()[0] - self.global_x, pygame.mouse.get_pos()[1] - self.global_y)

        if not self.image_loaded:
            return "No image loaded"
        elif not self.brush_down and not self.get_global_bounding_rect().collidepoint(pygame.mouse.get_pos()):
            return ""

        pos_x = int((mouse_pos[0] - self.scroll[0]) % (math.floor(self.loaded_image.get_width() * self.zoom)) / self.zoom)
        pos_y = int((mouse_pos[1] - self.scroll[1]) % (math.floor(self.loaded_image.get_height() * self.zoom)) / self.zoom)
        return f"Mouse position: ({pos_x}, {pos_y})"            

    def get_zoom_text(self):
        # Used by text objects to stay updated with the zoom level even as the self.zoom variable changes.
        return "Zoom: " + str(round(self.zoom * 100)) + "%"

    def increment_zoom(self):
        self.zoom += 0.1
        self.zoom = min(20, self.zoom)

    def decrement_zoom(self):
        self.zoom -= 0.1
        self.zoom = max(0.1, self.zoom)

    def open_file(self):
        # Block mouse before opening filedialog
        root = self
        while root.parent is not None: # Find root parent
            root = root.parent
        # Tell the root parent (which will tell the whole hierarchy) that the mouse is not hovering over it
        # This will block all mouse clicks until the next time the root has mouse_over() updated (which happens every frame)
        root.mouse_over(False) 
        
        filepath = filedialog.askopenfilename()
        try:
            self.loaded_image = pygame.image.load(filepath).convert_alpha()
            self.open_filepath = filepath
            self.image_loaded = True
        except FileNotFoundError:
            print("File not found.")
        except pygame.error:
            print("Error with file format.")

    def save_image(self):
        if self.image_loaded:
            pygame.image.save(self.loaded_image, self.open_filepath)

    def save_as(self):
        if self.image_loaded:
            # Block mouse before opening filedialog
            root = self
            while root.parent is not None: # Find root parent
                root = root.parent
            # Tell the root parent (which will tell the whole hierarchy) that the mouse is not hovering over it
            # This will block all mouse clicks until the next time the root has mouse_over() updated (which happens every frame)
            root.mouse_over(False) 
            
            filepath = filedialog.asksaveasfilename()
            try:
                pygame.image.save(self.loaded_image, filepath)
                self.loaded_image = pygame.image.load(filepath).convert_alpha()
                self.open_filepath = filepath
            except pygame.error:
                print(f"Invalid file format. Try '.png'")

    def render(self, surface):
        # Render and tile the loaded image onto the passed surface.
        if self.image_loaded:
            # Create a surface to render and tile the loaded image within a fixed region.
            temporary_surface = pygame.Surface(self.size)
            
            # Scale the loaded image to be rendered
            # This gets laggy when zoomed in due to large image sizes. This should be fixed in future versions.
            scaled_image = pygame.transform.scale(self.loaded_image, (self.loaded_image.get_width() * self.zoom, self.loaded_image.get_height() * self.zoom))

            # Apply the modulo function to the scroll to make the tiled image rendering appear continuous.
            self.scroll[0] %= -scaled_image.get_width()
            self.scroll[1] %= -scaled_image.get_height()

            # Tile and draw the image onto the temporary surface.
            for y in range(math.ceil(surface.get_height() / self.loaded_image.get_height() / self.zoom) + 2):
                for x in range(math.ceil(surface.get_width() / self.loaded_image.get_width() / self.zoom) + 2):
                    temporary_surface.blit(scaled_image, (x * math.floor(self.loaded_image.get_width() * self.zoom) + self.scroll[0], y * math.floor(self.loaded_image.get_height() * self.zoom) + self.scroll[1]))

            # Render the temporary surface onto the passed surface.
            surface.blit(temporary_surface, self.get_global_pos())

    def mouse_over(self, hovered):
        # Runs every frame. Set self.is_hovered.
        # hovered is True only if the mouse is over this canvas and is not being blocked by a UI element on a higher layer.        
        self.is_hovered = hovered

    def mouse_moved(self, mouse_rel):
        # Mouse position relative to the top left corner of the canvas
        mouse_pos = (pygame.mouse.get_pos()[0] - self.global_x, pygame.mouse.get_pos()[1] - self.global_y)
        mouse_move_distance = math.hypot(*mouse_rel)

        # Spacing between each painted spot along the line that was painted
        spacing = self.zoom # Scalar
        space = (mouse_rel[0] / mouse_move_distance * spacing, mouse_rel[1] / mouse_move_distance * spacing) # Vector with magnitude of spacing in the direction of mouse_rel

        # If an image is loaded and the brush is down, paint between the current position and the previous position
        if self.image_loaded and self.brush_down:
            # Paint along the line the mouse moved
            for i in range(max(1, int(mouse_move_distance / spacing))):
                center_pos_x = int((mouse_pos[0] - i * space[0] - self.scroll[0]) % (math.floor(self.loaded_image.get_width() * self.zoom)) / self.zoom)
                center_pos_y = int((mouse_pos[1] - i * space[1] - self.scroll[1]) % (math.floor(self.loaded_image.get_height() * self.zoom)) / self.zoom)
                if self.brush.shape == 'pixel':
                    self.loaded_image.set_at((center_pos_x, center_pos_y), self.brush.color)
                elif self.brush.shape == 'brush':
                    for dy in range(self.brush.size * 2 + 1):
                        for dx in range(self.brush.size * 2 + 1):
                            pos_x = (center_pos_x + dx - self.brush.size) % self.loaded_image.get_width()
                            pos_y = (center_pos_y + dy - self.brush.size) % self.loaded_image.get_height()
                            point_distance = math.dist(mouse_pos, (mouse_pos[0] + dx - self.brush.size, mouse_pos[1] + dy - self.brush.size))
                            if point_distance <= self.brush.size:
                                modules.utils.overlay_pixel(self.loaded_image, (pos_x, pos_y), (self.brush.color[0], self.brush.color[1], self.brush.color[2], self.brush.color[3] * (1 - point_distance / self.brush.size)))
                elif self.brush.shape == 'circle':
                    for dy in range(self.brush.size * 2 + 1):
                        for dx in range(self.brush.size * 2 + 1):
                            if math.dist(mouse_pos, (mouse_pos[0] + dx - self.brush.size, mouse_pos[1] + dy - self.brush.size)) <= self.brush.size:
                                pos_x = (center_pos_x + dx - self.brush.size) % self.loaded_image.get_width()
                                pos_y = (center_pos_y + dy - self.brush.size) % self.loaded_image.get_height()
                                self.loaded_image.set_at((pos_x, pos_y), self.brush.color)
            
    def left_mouse_down(self):
        # If the canvas was clicked
        if self.is_hovered:
            # If this canvas has a parent, move it to the top layer of canvases
            if self.parent is not None:
                self.parent.canvases.remove(self)
                self.parent.canvases.append(self)
                
            # The canvas was pressed, so the brush is down
            self.brush_down = True
            
            # Mouse position relative to the top left corner of the canvas
            mouse_pos = (pygame.mouse.get_pos()[0] - self.global_x, pygame.mouse.get_pos()[1] - self.global_y)

            # If an image is loaded, paint at the mouse position
            if self.image_loaded:
                # Calculate the pixel position on the canvas where the mouse is
                center_pos_x = int((mouse_pos[0] - self.scroll[0]) % (math.floor(self.loaded_image.get_width() * self.zoom)) / self.zoom)
                center_pos_y = int((mouse_pos[1] - self.scroll[1]) % (math.floor(self.loaded_image.get_height() * self.zoom)) / self.zoom)
                # Paint
                if self.brush.shape == 'pixel':
                    self.loaded_image.set_at((center_pos_x, center_pos_y), self.brush.color)
                elif self.brush.shape == 'brush':
                    for dy in range(self.brush.size * 2 + 1):
                        for dx in range(self.brush.size * 2 + 1):
                            pos_x = (center_pos_x + dx - self.brush.size) % self.loaded_image.get_width()
                            pos_y = (center_pos_y + dy - self.brush.size) % self.loaded_image.get_height()
                            point_distance = math.dist(mouse_pos, (mouse_pos[0] + dx - self.brush.size, mouse_pos[1] + dy - self.brush.size))
                            if point_distance <= self.brush.size:
                                modules.utils.overlay_pixel(self.loaded_image, (pos_x, pos_y), (self.brush.color[0], self.brush.color[1], self.brush.color[2], self.brush.color[3] * (1 - point_distance / self.brush.size)))
                elif self.brush.shape == 'circle':
                    for dy in range(self.brush.size * 2 + 1):
                        for dx in range(self.brush.size * 2 + 1):
                            if math.dist(mouse_pos, (mouse_pos[0] + dx - self.brush.size, mouse_pos[1] + dy - self.brush.size)) <= self.brush.size:
                                pos_x = (center_pos_x + dx - self.brush.size) % self.loaded_image.get_width()
                                pos_y = (center_pos_y + dy - self.brush.size) % self.loaded_image.get_height()
                                self.loaded_image.set_at((pos_x, pos_y), self.brush.color)

    def left_mouse_up(self):
        # The mouse was released, so the brush is not down
        self.brush_down = False
