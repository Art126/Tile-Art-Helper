## Author: Alexander Art

# Overlay a pixel on an image with a new color. Works with transparency.
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

## Globals (having the brush saved here is a temporary solution)
# Set up global brush
brush = 'pixel'
brush_color = (255, 0, 255, 255)
brush_size = 5
do_not_paint = False
