## Author: Alexander Art


# Tiling button

tiling_enabled = True

def toggle_tiling():
    global tiling_enabled
    tiling_enabled = not tiling_enabled


# Resize panel

resize_width = None
resize_height = None

def get_resize_width_text():
    global resize_width
    if resize_width is None:
        return "N/A"
    else:
        return str(resize_width)

def get_resize_height_text():
    global resize_height
    if resize_height is None:
        return "N/A"
    else:
        return str(resize_height)

def set_resize_width(new_resize_width):
    global resize_width
    try:
        if int(new_resize_width) > 0:
            resize_width = int(new_resize_width)
    except ValueError:
        pass

def set_resize_height(new_resize_height):
    global resize_height
    try:
        if int(new_resize_height) > 0:
            resize_height = int(new_resize_height)
    except ValueError:
        pass

def increase_resize_width():
    global resize_width
    if resize_width is not None:
        resize_width += 1

def increase_resize_height():
    global resize_height
    if resize_height is not None:
        resize_height += 1

def decrease_resize_width():
    global resize_width
    if resize_width is not None:
        if resize_width > 1:
            resize_width -= 1

def decrease_resize_height():
    global resize_height
    if resize_height is not None:
        if resize_height > 1:
            resize_height -= 1
