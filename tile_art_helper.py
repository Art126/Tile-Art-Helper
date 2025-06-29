## Tile Art Helper v0.3.2
## Author: Alexander Art

import pygame, tkinter, math
from tkinter import filedialog

# Class for panel UIs
class Panel:
    # If a panel is not fixed, it will have a title bar drawn above it so that it can be dragged around.
    title_bar_height = 10
    
    def __init__(self, rect, fixed, bgcolor=(127, 63, 0)):
        # This panel's parent object. This gets set with parent.add_panel(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and rendering/input functions must be called explicitly.
        self.parent = None
        
        # Create rect object from rect argument.
        rect = pygame.Rect(rect)

        # Create the panel surface.
        # Once created, the panel size is fixed. (Consider changing this in future versions!)
        self.surface = pygame.Surface(rect.size)

        # Position of the panel relative to the top left corner of its parent.
        self.local_x = rect.x
        self.local_y = rect.y

        # True if the panel should be fixed and not have a title bar.
        # False if the panel should have a title bar and be movable.
        self.fixed = fixed

        # Can be set with .set_caption()
        self.title = ""

        # If the panel is movable, this keeps track of when it is being moved.
        self.title_bar_held = False

        # Background color of the panel.
        # TODO: Implement color schemes.
        self.bgcolor = bgcolor

        # Panels, canvases, buttons, and text may be added as child objects.
        self.panels = []
        self.canvases = [] # Needing several canvases is rare.
        self.buttons = []
        self.text = []

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
            return pygame.Rect(self.local_x, self.local_y, self.surface.get_width(), self.surface.get_height())
        else:
            return pygame.Rect(self.local_x, self.local_y - self.title_bar_height, self.surface.get_width(), self.surface.get_height() + self.title_bar_height)

    def get_global_bounding_rect(self):
        if self.fixed:
            return pygame.Rect(self.global_x, self.global_y, self.surface.get_width(), self.surface.get_height())
        else:
            return pygame.Rect(self.global_x, self.global_y - self.title_bar_height, self.surface.get_width(), self.surface.get_height() + self.title_bar_height)

    def get_local_title_bar_rect(self):
        if self.fixed:
            return None
        else:
            return pygame.Rect(self.local_x, self.local_y - self.title_bar_height, self.surface.get_width(), self.title_bar_height)

    def get_global_title_bar_rect(self):
        if self.fixed:
            return None
        else:
            return pygame.Rect(self.global_x, self.global_y - self.title_bar_height, self.surface.get_width(), self.title_bar_height)

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

    def add_text(self, text):
        self.text.append(text)
        text.parent = self
        return self

    def render(self, surface):
        # If this panel is not fixed, draw the tittle bar and its caption onto the passed surface.
        if not self.fixed:
            pygame.draw.rect(surface, (255, 255, 255), (self.local_x, self.local_y - 10, self.surface.get_width(), 10))
            surface.blit(pygame.font.Font(None, 12).render(self.title, True, (0, 0, 0)), (self.local_x + 2, self.local_y - 9))

        # Render self.surface before blitting it onto the passed surface.

        # Clear panel surface
        self.surface.fill(self.bgcolor)

        # Render child canvases
        for canvas in self.canvases:
            canvas.render(self.surface)

        # Render child panels
        for panel in self.panels:
            panel.render(self.surface)

        # Render child buttons
        for button in self.buttons:
            button.render(self.surface)
            
        # Render child text
        for text in self.text:
            text.render(self.surface)

        # Blit the panel surface (self.surface) onto the given surface (surface)
        surface.blit(self.surface, (self.local_x, self.local_y))

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

    def left_mouse_down(self):
        # This function runs on the left mousedown event.

        if not clicks_blocked:
            # Detect when title bar is visible and is pressed
            if not self.fixed:
                if self.get_global_title_bar_rect().collidepoint(pygame.mouse.get_pos()):
                    self.title_bar_held = True

            # Pass mouse press to child panels
            for panel in self.panels:
                panel.left_mouse_down()

            # Child panels cover child canvases and can block them from being pressed
            for panel in self.panels:
                # Detect overlap
                if panel.get_global_bounding_rect().collidepoint(pygame.mouse.get_pos()):
                    break
            else:
                # Only runs if no child panels were pressed
                # Pass mouse press to child canvases
                for canvas in self.canvases:
                    canvas.left_mouse_down()

            # Pass mouse press to child buttons
            for button in self.buttons:
                button.left_mouse_down()

    def left_mouse_up(self):
        # This function runs on the left mouseup event.
        
        self.title_bar_held = False

        # To keep the title bar visible, ensure that the title bar is not dragged off the parent panel
        if not self.fixed:
            self.local_x = max(self.local_x, 0)
            self.local_x = min(self.local_x, self.parent.surface.get_width() - self.surface.get_width())
            self.local_y = max(self.local_y, self.title_bar_height)
            self.local_y = min(self.local_y, self.parent.surface.get_height())

        # Pass mouse up to child panels
        for panel in self.panels:
            panel.left_mouse_up()

        # Pass mouse up to child canvases
        for canvas in self.canvases:
            canvas.left_mouse_up()

# Class for canvas UI element
class Canvas:
    def __init__(self, rect):
        # This canvas's parent object. This gets set with parent.add_canvas(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and rendering/input functions must be called explicitly.
        self.parent = None

        # Create rect object from rect argument.
        rect = pygame.Rect(rect)

        # Create the panel surface.
        # Once created, the canvas size is fixed. (Consider changing this in future versions!)
        self.surface = pygame.Surface(rect.size)

        # Position of the canvas relative to the top left corner of its parent.
        self.local_x = rect.x
        self.local_y = rect.y

        self.zoom = 1 # zoom < 1 means zoomed out. zoom > 1 means zoomed in.
        self.scroll = [0, 0]

        self.loaded_image = None
        self.open_filepath = None
        self.image_loaded = False

        # True when the brush is being painted on the canvas.
        self.brush_down = False

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
        return pygame.Rect(self.local_x, self.local_y, self.surface.get_width(), self.surface.get_height())

    def get_global_bounding_rect(self):
        return pygame.Rect(self.global_x, self.global_y, self.surface.get_width(), self.surface.get_height())

    def get_coords_text(self):
        # Returns the coordinates of the mouse position on the canvas as text.
        # This assumes that the canvas is at (0, 0). Temporary solution!
        if self.image_loaded:
            pos_x = int((pygame.mouse.get_pos()[0] - self.scroll[0]) % (math.floor(self.loaded_image.get_width() * self.zoom)) / self.zoom)
            pos_y = int((pygame.mouse.get_pos()[1] - self.scroll[1]) % (math.floor(self.loaded_image.get_height() * self.zoom)) / self.zoom)
            return f"Mouse position: ({pos_x}, {pos_y})"
        else:
            return "No image loaded"

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
        # Block clicks before opening filedialog
        global clicks_blocked
        clicks_blocked = True
        
        filepath = tkinter.filedialog.askopenfilename()
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
            # Block clicks before opening filedialog
            global clicks_blocked
            clicks_blocked = True
            
            filepath = filedialog.asksaveasfilename()
            try:
                pygame.image.save(self.loaded_image, filepath)
                self.loaded_image = pygame.image.load(filepath).convert_alpha()
                self.open_filepath = filepath
            except pygame.error:
                print(f"Invalid file format. Try '.png'")

    def render(self, surface):
        # Render the loaded image
        if self.image_loaded:
            # Scale the loaded image to be rendered
            # This gets laggy when zoomed in due to large image sizes. This should be fixed in future versions.
            scaled_image = pygame.transform.scale(self.loaded_image, (self.loaded_image.get_width() * self.zoom, self.loaded_image.get_height() * self.zoom))

            # Apply the modulo function to the scroll to make the tiled image rendering appear continuous.
            self.scroll[0] %= -scaled_image.get_width()
            self.scroll[1] %= -scaled_image.get_height()

            # Tile and draw the image
            for y in range(math.ceil(surface.get_height() / self.loaded_image.get_height() / self.zoom) + 2):
                for x in range(math.ceil(surface.get_width() / self.loaded_image.get_width() / self.zoom) + 2):
                    self.surface.blit(scaled_image, (x * math.floor(self.loaded_image.get_width() * self.zoom) + self.scroll[0], y * math.floor(self.loaded_image.get_height() * self.zoom) + self.scroll[1]))

            # The rendered self.surface is blitted it onto the passed surface.
            surface.blit(self.surface, self.get_local_pos())

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
                if brush == 'pixel':
                    self.loaded_image.set_at((center_pos_x, center_pos_y), brush_color)
                elif brush == 'brush':
                    for dy in range(brush_size * 2 + 1):
                        for dx in range(brush_size * 2 + 1):
                            pos_x = (center_pos_x + dx - brush_size) % self.loaded_image.get_width()
                            pos_y = (center_pos_y + dy - brush_size) % self.loaded_image.get_height()
                            point_distance = math.dist(mouse_pos, (mouse_pos[0] + dx - brush_size, mouse_pos[1] + dy - brush_size))
                            if point_distance <= brush_size:
                                overlay_pixel(self.loaded_image, (pos_x, pos_y), (brush_color[0], brush_color[1], brush_color[2], brush_color[3] * (1 - point_distance / brush_size)))
                elif brush == 'circle':
                    for dy in range(brush_size * 2 + 1):
                        for dx in range(brush_size * 2 + 1):
                            if math.dist(mouse_pos, (mouse_pos[0] + dx - brush_size, mouse_pos[1] + dy - brush_size)) <= brush_size:
                                pos_x = (center_pos_x + dx - brush_size) % self.loaded_image.get_width()
                                pos_y = (center_pos_y + dy - brush_size) % self.loaded_image.get_height()
                                self.loaded_image.set_at((pos_x, pos_y), brush_color)
            
    def left_mouse_down(self):
        if not clicks_blocked:
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
                if brush == 'pixel':
                    self.loaded_image.set_at((center_pos_x, center_pos_y), brush_color)
                elif brush == 'brush':
                    for dy in range(brush_size * 2 + 1):
                        for dx in range(brush_size * 2 + 1):
                            pos_x = (center_pos_x + dx - brush_size) % self.loaded_image.get_width()
                            pos_y = (center_pos_y + dy - brush_size) % self.loaded_image.get_height()
                            point_distance = math.dist(mouse_pos, (mouse_pos[0] + dx - brush_size, mouse_pos[1] + dy - brush_size))
                            if point_distance <= brush_size:
                                overlay_pixel(self.loaded_image, (pos_x, pos_y), (brush_color[0], brush_color[1], brush_color[2], brush_color[3] * (1 - point_distance / brush_size)))
                elif brush == 'circle':
                    for dy in range(brush_size * 2 + 1):
                        for dx in range(brush_size * 2 + 1):
                            if math.dist(mouse_pos, (mouse_pos[0] + dx - brush_size, mouse_pos[1] + dy - brush_size)) <= brush_size:
                                pos_x = (center_pos_x + dx - brush_size) % self.loaded_image.get_width()
                                pos_y = (center_pos_y + dy - brush_size) % self.loaded_image.get_height()
                                self.loaded_image.set_at((pos_x, pos_y), brush_color)

    def left_mouse_up(self):
        # The mouse was released, so the brush is not down
        self.brush_down = False

# Class for button UI elements
class Button:
    def __init__(self, rect, action, label):
        # This button's parent object. This gets set with parent.add_button(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and rendering/input functions must be called explicitly.
        self.parent = None

        self.rect = pygame.Rect(rect) # Relative to parent
        self.action = action
        self.label = label
        
    def get_local_pos(self):
        return (self.local_x, self.local_y)

    def get_global_pos(self):
        if self.parent is not None:
            parent_pos = self.parent.get_global_pos() # Avoids redundant recursive calls
            return (parent_pos[0] + self.rect.x, parent_pos[1] + self.rect.y)
        else:
            return (self.rect.x, self.rect.y)

    @property
    def global_x(self):
        return self.get_global_pos()[0]

    @property
    def global_y(self):
        return self.get_global_pos()[1]

    def render(self, surface):
        # Mouse position relative to the top left corner of the parent
        mouse_pos = (pygame.mouse.get_pos()[0] - self.parent.global_x, pygame.mouse.get_pos()[1] - self.parent.global_y)

        # Change the button color if it is being hovered
        if self.rect.collidepoint(mouse_pos):
            color = (255, 127, 63)
        else:
            color = (63, 0, 0)

        # Draw button bounding rect
        pygame.draw.rect(surface, color, self.rect)

        # Draw button label
        surface.blit(pygame.font.Font(None, 16).render(self.label, True, (255, 255, 255)), (self.rect.x + 4, self.rect.y + 3))

    def left_mouse_down(self):
        # Mouse position relative to the top left corner of the parent
        mouse_pos = (pygame.mouse.get_pos()[0] - self.parent.global_x, pygame.mouse.get_pos()[1] - self.parent.global_y)

        # If this button is pressed, run its function.
        if self.rect.collidepoint(mouse_pos):
            self.action()

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
        surface.blit(pygame.font.Font(None, self.size).render(message, True, self.color), self.get_local_pos())

# Works with transparency
def overlay_pixel(image_source, pos, color):
    # Get previous color to overlay
    previous_color = image_source.get_at(pos)

    # Lazy color blending algorithm
    new_color = ((previous_color[0] * (1 - color[3] / 255) + color[0] * color[3] / 255) // 1, (previous_color[1] * (1 - color[3] / 255) + color[1] * color[3] / 255) // 1, (previous_color[2] * (1 - color[3] / 255) + color[2] * color[3] / 255) // 1, previous_color[3])

    # Set the pixel
    image_source.set_at(pos, new_color)

def get_brush_size_text():
    return str(brush_size)

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

# Set up global brush
brush = 'pixel'
brush_color = (255, 0, 255, 255)
brush_size = 5
do_not_paint = False

# Used for blocking input upon exiting filedialog
clicks_blocked = False

def main():
    print("INSTRUCTIONS:")
    print("Open an image file")
    print("Left click to paint")
    print("Middle click to use a color picker at the mouse position")
    print("Right click and drag to pan")
    print("Scroll to zoom")
    print("Use the on-screen controls for everything else")
    

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Tile Art Helper")
    display = pygame.display.set_mode((640, 360), pygame.SCALED)


    # Create root (main) panel
    main_panel = Panel((0, 0, 0, 0), True, (0, 0, 0))

    # Set the main panel to render directly to the display surface
    main_panel.surface = display


    # Create the main canvas and make it a child of the main panel
    canvas = Canvas((0, 0, display.get_width(), display.get_height()))
    main_panel.add_canvas(canvas)


    # Create a top panel and make it a child of the main panel
    top_panel = Panel((0, 0, display.get_width(), 30), True)
    main_panel.add_panel(top_panel)

    # Top panel save options
    open_image_button = Button((2, 2, 80, 20), canvas.open_file, "Open Image")
    top_panel.add_button(open_image_button)
    save_overwrite_button = Button((102, 2, 80, 20), canvas.save_image, "Save")
    top_panel.add_button(save_overwrite_button)
    save_overwrite_text = Text("Will overwrite previous!", 12, (255, 255, 255), (97, 22))
    top_panel.add_text(save_overwrite_text)
    save_as_button = Button((202, 2, 80, 20), canvas.save_as, "Save As")
    top_panel.add_button(save_as_button)

    
    # Create bottom panel and make it a child of the main panel
    bottom_panel = Panel((0, display.get_height() - 15, display.get_width(), 15), True)
    main_panel.add_panel(bottom_panel)

    # Bottom panel coordinate text
    coords_text = Text(canvas.get_coords_text, 12, (255, 255, 255), (4, 3))
    bottom_panel.add_text(coords_text)

    # Bottom panel zoom buttons and text
    zoom_text = Text(canvas.get_zoom_text, 12, (255, 255, 255), (display.get_width() - 80, 3))
    bottom_panel.add_text(zoom_text)
    increment_zoom_button = Button((display.get_width() - 30, 1, 13, 13), canvas.increment_zoom, "+")
    bottom_panel.add_button(increment_zoom_button)
    decrement_zoom_button = Button((display.get_width() - 95, 1, 13, 13), canvas.decrement_zoom, "-")
    bottom_panel.add_button(decrement_zoom_button)


    # Create tools panel and make it a child of the main panel
    tools_panel = Panel((display.get_width() - 110, 50, 100, 130), False).set_caption("Brush tools")
    main_panel.add_panel(tools_panel)

    # Tools panel brush options
    pixel_button = Button((10, 10, 80, 20), set_brush_pixel, "Pixel")
    tools_panel.add_button(pixel_button)
    brush_button = Button((10, 40, 80, 20), set_brush_brush, "Brush")
    tools_panel.add_button(brush_button)
    circle_button = Button((10, 70, 80, 20), set_brush_circle, "Circle")
    tools_panel.add_button(circle_button)

    # Tools panel brush size settings and text
    brush_size_text = Text(get_brush_size_text, 16, (255, 255, 255), (45, 105))
    tools_panel.add_text(brush_size_text)
    increase_brush_size_button = Button((70, 100, 20, 20), increase_brush_size, "+")
    tools_panel.add_button(increase_brush_size_button)
    decrease_brush_size_button = Button((10, 100, 20, 20), decrease_brush_size, "-")
    tools_panel.add_button(decrease_brush_size_button)


    # Frame loop (repeats every frame the program is open)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEMOTION:
                main_panel.mouse_moved(event.rel)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    main_panel.left_mouse_down()
                if event.button == 2:
                    if canvas.image_loaded:
                        # Pick the color at the mouse position
                        global brush_color
                        brush_color = canvas.loaded_image.get_at((int((event.pos[0] - canvas.scroll[0]) % math.floor(canvas.loaded_image.get_width() * canvas.zoom) / canvas.zoom), int((event.pos[1] - canvas.scroll[1]) % math.floor(canvas.loaded_image.get_height() * canvas.zoom) / canvas.zoom)))
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    main_panel.left_mouse_up()
            if event.type == pygame.MOUSEWHEEL:
                # Zooming
                # If the mouse wheel is scrolled, manually update the canvas's zoom.
                
                # Keep track of the mouse position before the zoom, needed for centering the zoom at the mouse position.
                # Keep in mind that scroll is negative.
                previous_scaled_mouse_pos = (canvas.scroll[0] / canvas.zoom - pygame.mouse.get_pos()[0] / canvas.zoom, canvas.scroll[1] / canvas.zoom - pygame.mouse.get_pos()[1] / canvas.zoom)

                # Adjust scale (zooms in/out)
                canvas.zoom += event.y / 10 * canvas.zoom

                # Limit how far the user can zoom in
                canvas.zoom = min(20, canvas.zoom)

                # Limit how far the user can be zoom out
                canvas.zoom = max(0.1, canvas.zoom)

                # Round the zoom to the nearest percent
                canvas.zoom = round(canvas.zoom, 2)

                # Center the zooming action at the mouse position.
                new_scaled_mouse_pos = (canvas.scroll[0] / canvas.zoom - pygame.mouse.get_pos()[0] / canvas.zoom, canvas.scroll[1] / canvas.zoom - pygame.mouse.get_pos()[1] / canvas.zoom)
                canvas.scroll[0] += (previous_scaled_mouse_pos[0] - new_scaled_mouse_pos[0]) * canvas.zoom
                canvas.scroll[1] += (previous_scaled_mouse_pos[1] - new_scaled_mouse_pos[1]) * canvas.zoom

                        
        # Panning

        # If the right mouse button is pressed, manually update the canvas's scroll based on mouse movement.
        if pygame.mouse.get_pressed()[2]:
            canvas.scroll[0] += pygame.mouse.get_pos()[0] - previous_mouse_pos[0]
            canvas.scroll[1] += pygame.mouse.get_pos()[1] - previous_mouse_pos[1]

        previous_mouse_pos = pygame.mouse.get_pos() # pygame.mouse.get_rel() does not take into account pygame.SCALED
        

        # clicks_blocked is only needed for one frame.
        global clicks_blocked
        clicks_blocked = False
        

        # Rendering

        # Clear display
        display.fill((0, 0, 0))

        # Render main panel
        main_panel.render(display)

        # Update pygame display and tick the pygame clock
        pygame.display.update()
        pygame.time.Clock().tick(60)

    # Loop exited
    pygame.quit()    

if __name__ == '__main__':
    main()
