## Tile Art Helper v0.2.0
## Author: Alexander Art

import pygame, tkinter, math
from tkinter import filedialog

print("INSTRUCTIONS:")
print("Open an image file")
print("Left click to paint")
print("Middle click to use a color picker at the mouse position")
print("Right click and drag to pan")
print("Scroll to zoom")
print("Use the on-screen controls for everything else")

pygame.init()
pygame.display.set_caption('Tile Art Helper')
display = pygame.display.set_mode((640, 360), pygame.SCALED)

# Class for panel UIs
class Panel:
    def __init__(self, rect):
        rect = pygame.Rect(rect)
        self.surface = pygame.Surface(rect.size)
        self.x = rect.x
        self.y = rect.y
        self.buttons = []
        self.text = []

    def add_button(self, button):
        self.buttons.append(button)

    def add_text(self, pos, message):
        # This should probably be replaced with some kind of text object in future versions.
        self.text.append([pos, message])

    def render(self, surface, mouse_pos):
        self.surface.fill((127, 63, 0))
        
        for button in self.buttons:
            button.render(self.surface, (mouse_pos[0] - self.x, mouse_pos[1] - self.y))
            
        for text in self.text:
            # If the string is given by a function, then call the function.
            # Otherwise, render the text as usual.
            if callable(text[1]):
                self.surface.blit(pygame.font.Font(None, 12).render(text[1](), True, (255, 255, 255)), text[0])
            else:
                self.surface.blit(pygame.font.Font(None, 12).render(text[1], True, (255, 255, 255)), text[0])

        surface.blit(self.surface, (self.x, self.y))

    def left_mouse_down(self, mouse_pos):
        for button in self.buttons:
            button.left_mouse_down((mouse_pos[0] - self.x, mouse_pos[1] - self.y))

# Class for button UI elements
class Button:
    def __init__(self, rect, action, text):
        self.rect = pygame.Rect(rect)
        self.action = action
        self.text = text

    def render(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            color = (255, 127, 63)
        else:
            color = (63, 0, 0)
            
        pygame.draw.rect(surface, color, self.rect)
        
        surface.blit(pygame.font.Font(None, 16).render(self.text, True, (255, 255, 255)), (self.rect.x + 4, self.rect.y + 3))

    def left_mouse_down(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()

def open_file():
    global loaded_image, open_filepath, image_loaded
    filepath = tkinter.filedialog.askopenfilename()
    try:
        loaded_image = pygame.image.load(filepath).convert_alpha()
        open_filepath = filepath
        image_loaded = True
    except FileNotFoundError:
        print("File not found.")
    except pygame.error:
        print("Error with file format.")

def save_image():
    if image_loaded:
        pygame.image.save(loaded_image, open_filepath)

def save_as():
    if image_loaded:
        global loaded_image, open_filepath
        filepath = filedialog.asksaveasfilename()
        try:
            pygame.image.save(loaded_image, filepath)
            loaded_image = pygame.image.load(filepath).convert_alpha()
            open_filepath = filepath
        except pygame.error:
            print(f"Invalid file format. Try '.png'")

# Works with transparency
def overlay_pixel(image_source, pos, color):
    # Get previous color to overlay
    previous_color = image_source.get_at(pos)

    # Lazy color blending algorithm
    new_color = ((previous_color[0] * (1 - color[3] / 255) + color[0] * color[3] / 255) // 1, (previous_color[1] * (1 - color[3] / 255) + color[1] * color[3] / 255) // 1, (previous_color[2] * (1 - color[3] / 255) + color[2] * color[3] / 255) // 1, previous_color[3])

    # Set the pixel
    image_source.set_at(pos, new_color)

# Set brush to pixel mode
def set_brush_pixel():
    global brush
    brush = 'pixel'

# Set brush to brush mode (softer than circle mode)
def set_brush_brush():
    global brush
    brush = 'brush'

# Set brush to circle mode
def set_brush_circle():
    global brush
    brush = 'circle'

def increase_brush_size():
    global brush_size
    brush_size += 1

def decrease_brush_size():
    global brush_size
    brush_size -= 1
    brush_size = max(1, brush_size)

# Used by text to stay updated with the scale even as the variable changes
def get_zoom_text():
    return "Zoom: " + str(round(scale * 100)) + "%"

def increment_zoom():
    global scale
    scale += 0.1

def decrement_zoom():
    global scale
    scale -= 0.1
    scale = max(0.2, scale)

# Returns the coordinates of the mouse position on the canvas as text
def get_coords_text():
    if image_loaded:
        pos_x = int((pygame.mouse.get_pos()[0] - scroll[0]) % (math.floor(loaded_image.get_width() * scale)) / scale)
        pos_y = int((pygame.mouse.get_pos()[1] - scroll[1]) % (math.floor(loaded_image.get_height() * scale)) / scale)
        return f"Mouse position: ({pos_x}, {pos_y})"
    else:
        return "No image loaded"

tools_panel = Panel((10, 10, 200, 120))

open_image_button = Button((10, 10, 80, 20), open_file, "Open Image")
tools_panel.add_button(open_image_button)
save_overwrite_button = Button((10, 40, 80, 20), save_image, "Save")
tools_panel.add_button(save_overwrite_button)
tools_panel.add_text((5, 60), "Will overwrite previous!")
save_as_button = Button((10, 80, 80, 20), save_as, "Save As")
tools_panel.add_button(save_as_button)

pixel_button = Button((110, 10, 80, 20), set_brush_pixel, "Pixel")
tools_panel.add_button(pixel_button)
brush_button = Button((110, 40, 80, 20), set_brush_brush, "Brush")
tools_panel.add_button(brush_button)
circle_button = Button((110, 70, 80, 20), set_brush_circle, "Circle")
tools_panel.add_button(circle_button)

increase_brush_size_button = Button((170, 95, 20, 20), increase_brush_size, "+")
tools_panel.add_button(increase_brush_size_button)
decrease_brush_size_button = Button((110, 95, 20, 20), decrease_brush_size, "-")
tools_panel.add_button(decrease_brush_size_button)

bottom_panel = Panel((0, display.get_height() - 15, display.get_width(), 15))

bottom_panel.add_text((4, 3), get_coords_text)

bottom_panel.add_text((display.get_width() - 80, 3), get_zoom_text)
increment_zoom_button = Button((display.get_width() - 30, 1, 13, 13), increment_zoom, "+")
bottom_panel.add_button(increment_zoom_button)
decrement_zoom_button = Button((display.get_width() - 95, 1, 13, 13), decrement_zoom, "-")
bottom_panel.add_button(decrement_zoom_button)

panels = [
    tools_panel,
    bottom_panel
]

scale = 1
scroll = [0, 0]

loaded_image = None
open_filepath = None
image_loaded = False

brush = 'pixel'
brush_color = (255, 0, 255, 255)
brush_size = 5
do_not_paint = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for panel in panels:
                    panel.left_mouse_down(event.pos)
            if event.button == 2:
                # Pick the color at the mouse position
                brush_color = loaded_image.get_at((int((event.pos[0] - scroll[0]) % math.floor(loaded_image.get_width() * scale) / scale), int((event.pos[1] - scroll[1]) % math.floor(loaded_image.get_height() * scale) / scale)))
        if event.type == pygame.MOUSEWHEEL:
            scale += event.y / 10
            scale = max(0.2, scale)

    # Painting
    
    if pygame.mouse.get_pressed()[0] == True:
        if image_loaded:
            for panel in panels: # Ensure that painting does not occur when the mouse clicks on a panel instead of the canvas.
                if pygame.Rect((panel.x, panel.y), panel.surface.get_size()).collidepoint(pygame.mouse.get_pos()):
                    break
            else:
                # Paint
                if brush == 'pixel':
                    pos_x = int((pygame.mouse.get_pos()[0] - scroll[0]) % (math.floor(loaded_image.get_width() * scale)) / scale)
                    pos_y = int((pygame.mouse.get_pos()[1] - scroll[1]) % (math.floor(loaded_image.get_height() * scale)) / scale)
                    loaded_image.set_at((pos_x, pos_y), brush_color)
                elif brush == 'brush':
                    center_pos_x = int((pygame.mouse.get_pos()[0] - scroll[0]) % (math.floor(loaded_image.get_width() * scale)) / scale)
                    center_pos_y = int((pygame.mouse.get_pos()[1] - scroll[1]) % (math.floor(loaded_image.get_height() * scale)) / scale)
                    for dy in range(brush_size * 2 + 1):
                        for dx in range(brush_size * 2 + 1):
                            pos_x = (center_pos_x + dx - brush_size) % loaded_image.get_width()
                            pos_y = (center_pos_y + dy - brush_size) % loaded_image.get_height()
                            point_distance = math.dist(pygame.mouse.get_pos(), (pygame.mouse.get_pos()[0] + dx - brush_size, pygame.mouse.get_pos()[1] + dy - brush_size))
                            if point_distance <= brush_size:
                                overlay_pixel(loaded_image, (pos_x, pos_y), (brush_color[0], brush_color[1], brush_color[2], brush_color[3] * (1 - point_distance / brush_size)))
                elif brush == 'circle':
                    center_pos_x = int((pygame.mouse.get_pos()[0] - scroll[0]) % (math.floor(loaded_image.get_width() * scale)) / scale)
                    center_pos_y = int((pygame.mouse.get_pos()[1] - scroll[1]) % (math.floor(loaded_image.get_height() * scale)) / scale)
                    for dy in range(brush_size * 2 + 1):
                        for dx in range(brush_size * 2 + 1):
                            if math.dist(pygame.mouse.get_pos(), (pygame.mouse.get_pos()[0] + dx - brush_size, pygame.mouse.get_pos()[1] + dy - brush_size)) <= brush_size:
                                pos_x = (center_pos_x + dx - brush_size) % loaded_image.get_width()
                                pos_y = (center_pos_y + dy - brush_size) % loaded_image.get_height()
                                loaded_image.set_at((pos_x, pos_y), brush_color)
                                
    # Scrolling

    if pygame.mouse.get_pressed()[2] == True:
        scroll[0] += pygame.mouse.get_pos()[0] - previous_mouse_pos[0]
        scroll[1] += pygame.mouse.get_pos()[1] - previous_mouse_pos[1]

    previous_mouse_pos = pygame.mouse.get_pos() # pygame.mouse.get_rel() does not take into account pygame.SCALED

    # Rendering
    
    display.fill((0, 0, 0))
    
    if image_loaded:
        scaled_image = pygame.transform.scale(loaded_image, (loaded_image.get_width() * scale, loaded_image.get_height() * scale))

        scroll[0] = scroll[0] % -scaled_image.get_width()
        scroll[1] = scroll[1] % -scaled_image.get_height()

        cursor_y = 0
        for y in range(math.ceil(display.get_height() / loaded_image.get_height() / scale) + 2):
            cursor_x = 0
            for x in range(math.ceil(display.get_width() / loaded_image.get_width() / scale) + 2):
                display.blit(scaled_image, (cursor_x  + scroll[0], cursor_y + scroll[1]))
                cursor_x += math.floor(loaded_image.get_width() * scale)
            cursor_y += math.floor(loaded_image.get_height() * scale)
            
    for panel in panels:
        panel.render(display, pygame.mouse.get_pos())
        
    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()
