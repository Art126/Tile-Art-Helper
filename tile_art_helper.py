## Tile Art Helper v0.5.0
## Author: Alexander Art

import math

import pygame

import modules.settings
from modules.brush import Brush
from modules.ui.ui_style import Style
from modules.ui.panel import Panel
from modules.ui.canvas import Canvas
from modules.ui.button import Button
from modules.ui.text import Text
from modules.ui.slider import Slider

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
    display = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)


    # Create root (main) panel
    main_panel = Panel(((0, 0), display.get_size()), True, Style(panel_bg_color=(0, 0, 0)))


    # Create brush object
    brush = Brush()


    # Create the main canvas (including telling it which brush object to use)
    canvas = Canvas((0, 0, display.get_width(), display.get_height()), brush)
    # Make the main canvas a child of the main panel
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
    pixel_button = Button((20, 20, 160, 40), brush.set_brush_pixel, "Pixel")
    tools_panel.add_button(pixel_button)
    brush_button = Button((20, 80, 160, 40), brush.set_brush_brush, "Brush")
    tools_panel.add_button(brush_button)
    circle_button = Button((20, 140, 160, 40), brush.set_brush_circle, "Circle")
    tools_panel.add_button(circle_button)

    # Tools panel brush size settings and text
    brush_size_title_text = Text("Size", 32, (255, 255, 255), (72, 200))
    tools_panel.add_text(brush_size_title_text)
    brush_size_text = Text(brush.get_brush_size_text, 32, (255, 255, 255), (90, 230))
    tools_panel.add_text(brush_size_text)
    increase_brush_size_button = Button((140, 220, 40, 40), brush.increase_brush_size, "+", Style(button_text_size=48, button_text_padding=(10, 1)))
    tools_panel.add_button(increase_brush_size_button)
    decrease_brush_size_button = Button((20, 220, 40, 40), brush.decrease_brush_size, "-", Style(button_text_size=48, button_text_padding=(14, 2)))
    tools_panel.add_button(decrease_brush_size_button)

    # Color selector settings and text
    brush_color_text = Text("Color", 32, brush.color, (70, 280))
    tools_panel.add_text(brush_color_text)
    brush_rgb_text = Text("R             G             B", 24, (255, 255, 255), (32, 300))
    tools_panel.add_text(brush_rgb_text)
    red_slider = Slider((32, 320), 0, 255, (255, 0, 0))
    tools_panel.add_slider(red_slider)
    red_slider.percentage = brush.color[0] / 255 # Set default red value
    green_slider = Slider((96, 320), 0, 255, (0, 255, 0))
    tools_panel.add_slider(green_slider)
    green_slider.percentage = brush.color[1] / 255 # Set default green value
    blue_slider = Slider((160, 320), 0, 255, (0, 0, 255))
    tools_panel.add_slider(blue_slider)
    blue_slider.percentage = brush.color[2] / 255 # Set default blue value


    # Tools panel toggle visibility button
    toggle_brush_tools_button = Button((display.get_width() - 164, 4, 160, 40), tools_panel.toggle_visibility, "Brush tools")
    top_panel.add_button(toggle_brush_tools_button)


    # Toggle tiling button
    toggle_tiling_button = Button((display.get_width() - 328, 4, 160, 40), modules.settings.toggle_tiling, "Toggle tiling")
    top_panel.add_button(toggle_tiling_button)


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
                if event.key == pygame.K_o and event.mod & pygame.KMOD_CTRL:
                    canvas.open_file()
                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    if event.mod & pygame.KMOD_SHIFT:
                        canvas.save_as()
                    else:
                        canvas.save_image()
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
        brush.color = (red_slider.get_value(), green_slider.get_value(), blue_slider.get_value(), 255)
        brush_color_text.color = brush.color
        

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
