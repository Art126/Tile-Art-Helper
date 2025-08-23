## Tile Art Helper v0.4.3
## Author: Alexander Art

import pygame, tkinter, math
from tkinter import filedialog

# Class for UI element styles
class Style:
    def __init__(self,
                 panel_bg_color=(127, 63, 0),
                 panel_title_bar_color=(255, 255, 255),
                 panel_title_bar_text_color=(0, 0, 0),
                 panel_title_bar_text_size=24,
                 panel_title_bar_height=20,
                 button_default_bg_color=(63, 0, 0),
                 button_hovered_bg_color=(255, 127, 63),
                 button_default_text_color=(255, 255, 255),
                 button_hovered_text_color=(255, 255, 255),
                 button_text_size=32,
                 button_text_padding=(9, 9)):
        self.panel_bg_color = panel_bg_color
        self.panel_title_bar_color = panel_title_bar_color
        self.panel_title_bar_text_color = panel_title_bar_text_color
        self.panel_title_bar_text_size = panel_title_bar_text_size
        self.panel_title_bar_height = panel_title_bar_height
        self.button_default_bg_color = button_default_bg_color
        self.button_hovered_bg_color = button_hovered_bg_color
        self.button_default_text_color = button_default_text_color
        self.button_hovered_text_color = button_hovered_text_color
        self.button_text_size = button_text_size
        self.button_text_padding = button_text_padding

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

# Class for canvas UI element
class Canvas:
    def __init__(self, rect):
        # This canvas's parent object. This gets set with parent.add_canvas(self).
        # If the parent is a pygame surface instead of a panel, self.parent should remain None and rendering/input functions must be called explicitly.
        self.parent = None

        # Create rect object from rect argument.
        # Rect left (x) and top (y) values become the local x and y values for the canvas.
        self.rect = pygame.Rect(rect)

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

# Works with transparency
def overlay_pixel(image_source, pos, color):
    # Get previous color to overlay
    previous_color = image_source.get_at(pos)

    # Color blending (I don't know how I should go about blending the transparency)
    new_red = (previous_color[0] ** 2 * (1 - color[3] / 255) + color[0] ** 2 * color[3] / 255) ** (1 / 2)
    new_green = (previous_color[1] ** 2 * (1 - color[3] / 255) + color[1] ** 2 * color[3] / 255) ** (1 / 2)
    new_blue = (previous_color[2] ** 2 * (1 - color[3] / 255) + color[2] ** 2 * color[3] / 255) ** (1 / 2)
    new_color = (new_red, new_green, new_blue, previous_color[3])

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

def main():
    global brush_color
    
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
    display = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)


    # Create root (main) panel
    main_panel = Panel(((0, 0), display.get_size()), True, Style(panel_bg_color=(0, 0, 0)))


    # Create the main canvas and make it a child of the main panel
    canvas = Canvas((0, 0, display.get_width(), display.get_height()))
    main_panel.add_canvas(canvas)


    # Create a top panel and make it a child of the main panel
    top_panel = Panel((0, 0, display.get_width(), 60), True)
    main_panel.add_panel(top_panel)

    # Top panel save options
    open_image_button = Button((4, 4, 160, 40), canvas.open_file, "Open Image")
    top_panel.add_button(open_image_button)
    save_overwrite_button = Button((204, 4, 160, 40), canvas.save_image, "Save")
    top_panel.add_button(save_overwrite_button)
    save_overwrite_text = Text("Will overwrite previous!", 20, (255, 255, 255), (208, 45))
    top_panel.add_text(save_overwrite_text)
    save_as_button = Button((404, 4, 160, 40), canvas.save_as, "Save As")
    top_panel.add_button(save_as_button)

    
    # Create bottom panel and make it a child of the main panel
    bottom_panel = Panel((0, display.get_height() - 30, display.get_width(), 30), True)
    main_panel.add_panel(bottom_panel)

    # Bottom panel coordinate text
    coords_text = Text(canvas.get_coords_text, 24, (255, 255, 255), (8, 8))
    bottom_panel.add_text(coords_text)

    # Bottom panel zoom buttons and text
    zoom_text = Text(canvas.get_zoom_text, 24, (255, 255, 255), (display.get_width() - 160, 8))
    bottom_panel.add_text(zoom_text)
    increment_zoom_button = Button((display.get_width() - 60, 2, 26, 26), canvas.increment_zoom, "+", Style(button_text_padding=(6, 1)))
    bottom_panel.add_button(increment_zoom_button)
    decrement_zoom_button = Button((display.get_width() - 190, 2, 26, 26), canvas.decrement_zoom, "-", Style(button_text_padding=(9, 2)))
    bottom_panel.add_button(decrement_zoom_button)


    # Create tools panel and make it a child of the main panel
    tools_panel = Panel((display.get_width() - 220, 100, 200, 400), False).set_caption("Brush tools")
    main_panel.add_panel(tools_panel)

    # Tools panel brush options
    pixel_button = Button((20, 20, 160, 40), set_brush_pixel, "Pixel")
    tools_panel.add_button(pixel_button)
    brush_button = Button((20, 80, 160, 40), set_brush_brush, "Brush")
    tools_panel.add_button(brush_button)
    circle_button = Button((20, 140, 160, 40), set_brush_circle, "Circle")
    tools_panel.add_button(circle_button)

    # Tools panel brush size settings and text
    brush_size_title_text = Text("Size", 32, (255, 255, 255), (72, 200))
    tools_panel.add_text(brush_size_title_text)
    brush_size_text = Text(get_brush_size_text, 32, (255, 255, 255), (90, 230))
    tools_panel.add_text(brush_size_text)
    increase_brush_size_button = Button((140, 220, 40, 40), increase_brush_size, "+", Style(button_text_size=48, button_text_padding=(10, 1)))
    tools_panel.add_button(increase_brush_size_button)
    decrease_brush_size_button = Button((20, 220, 40, 40), decrease_brush_size, "-", Style(button_text_size=48, button_text_padding=(14, 2)))
    tools_panel.add_button(decrease_brush_size_button)

    # Color selector settings and text
    brush_color_text = Text("Color", 32, brush_color, (70, 280))
    tools_panel.add_text(brush_color_text)
    brush_rgb_text = Text("R             G             B", 24, (255, 255, 255), (32, 300))
    tools_panel.add_text(brush_rgb_text)
    red_slider = Slider((32, 320), 0, 255, (255, 0, 0))
    tools_panel.add_slider(red_slider)
    red_slider.percentage = brush_color[0] / 255 # Set default red value
    green_slider = Slider((96, 320), 0, 255, (0, 255, 0))
    tools_panel.add_slider(green_slider)
    green_slider.percentage = brush_color[1] / 255 # Set default green value
    blue_slider = Slider((160, 320), 0, 255, (0, 0, 255))
    tools_panel.add_slider(blue_slider)
    blue_slider.percentage = brush_color[2] / 255 # Set default blue value


    # Tools panel toggle visibility button
    toggle_brush_tools_button = Button((display.get_width() - 164, 4, 160, 40), tools_panel.toggle_visibility, "Brush tools")
    top_panel.add_button(toggle_brush_tools_button)


    # Frame loop (repeats every frame the program is open)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                # When the window is resized, resize and move every UI element that is based on the display size.
                main_panel.size = display.get_size()
                
                canvas.size = display.get_size()
                
                top_panel.width = display.get_width()
                
                bottom_panel.local_y = display.get_height() - 30
                bottom_panel.width = display.get_width()
                zoom_text.local_x = display.get_width() - 160
                increment_zoom_button.local_x = display.get_width() - 60
                decrement_zoom_button.local_x = display.get_width() - 190
                toggle_brush_tools_button.local_x = display.get_width() - 164

                tools_panel.keep_on_screen()
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
                        # Pick the color at the mouse position (alpha not yet supported)
                        new_color = canvas.loaded_image.get_at((int((event.pos[0] - canvas.scroll[0]) % math.floor(canvas.loaded_image.get_width() * canvas.zoom) / canvas.zoom), int((event.pos[1] - canvas.scroll[1]) % math.floor(canvas.loaded_image.get_height() * canvas.zoom) / canvas.zoom)))
                        red_slider.percentage = new_color[0] / 255
                        green_slider.percentage = new_color[1] / 255
                        blue_slider.percentage = new_color[2] / 255
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

        # Calculate which UI element(s) the mouse is hovering over (if any)
        main_panel.mouse_over(main_panel.get_global_bounding_rect().collidepoint(pygame.mouse.get_pos()))

                        
        # Panning

        # If the right mouse button is pressed, manually update the canvas's scroll based on mouse movement.
        if pygame.mouse.get_pressed()[2]:
            canvas.scroll[0] += pygame.mouse.get_pos()[0] - previous_mouse_pos[0]
            canvas.scroll[1] += pygame.mouse.get_pos()[1] - previous_mouse_pos[1]

        previous_mouse_pos = pygame.mouse.get_pos() # pygame.mouse.get_rel() does not take into account pygame.SCALED


        # Update brush color
        brush_color = (red_slider.get_value(), green_slider.get_value(), blue_slider.get_value(), 255)
        brush_color_text.color = brush_color
        

        # Rendering

        # Clear display
        display.fill((0, 0, 0))

        # Render main panel and all its children
        main_panel.render(display)

        # Update pygame display and tick the pygame clock
        pygame.display.update()
        pygame.time.Clock().tick(60)

    # Loop exited
    pygame.quit()    

if __name__ == '__main__':
    main()
