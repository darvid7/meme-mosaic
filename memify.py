from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw

import os

import urllib.request as ur
import sys
import math
import io
import os

# with open('t.jpg', 'wb') as f:
#     data = ur.urlopen('http://www.gunnerkrigg.com//comics/00000001.jpg').read()
#     print(data)
#     f.write(data)


def tint_image(image, tint_colour):
    new_image = ImageChops.multiply(image, Image.new('RGB', image.size, tint_colour))
    return new_image


def get_meme_image_from_url(url):
    binary_meme_data = ur.urlopen(url).read()
    meme_byte_stream = io.BytesIO(binary_meme_data)
    meme_image = Image.open(meme_byte_stream)
    return meme_image


def resize_image(original_image, scale_factor):
    x, y = original_image.size
    scaled_x = x * scale_factor
    scaled_y = y * scale_factor

    return original_image.resize((int(scaled_x), int(scaled_y)),Image.ANTIALIAS)
    # scaled_image = original_image.resize([int(scale_factor * s) for s in original_image.size])
    # return scaled_image


def get_avg_colour_of_section(image_object, current_col, section_col_max, current_row, section_row_max):
    pixel_aggregate = [0, 0, 0]
    iterations = 0
    for c in range(current_col, section_col_max):
        for r in range(current_row, section_row_max):
            red, green, blue = image_object[c, r]
            pixel_aggregate[0] += red
            pixel_aggregate[1] += green
            pixel_aggregate[2] += blue
            iterations += 1
    if iterations == 0:
        return [0 ,0, 0]
    pixel_avg = [int(val/iterations) for val in pixel_aggregate]
    # print('pixel avg: ' + str(pixel_avg))
    return pixel_avg

def write_to_meme_image(canvas_image_object, meme_image, meme_image_object, tile_image, meme_col_range, meme_row_range, current_col, next_col_bounds, current_row, next_row_bounds):
    if next_col_bounds >= meme_col_range:
        next_col_bounds = meme_col_range -1
    if next_row_bounds >= meme_row_range:
        next_row_bounds = meme_row_range -1

    # Will never give index error.
    section_avg = get_avg_colour_of_section(meme_image_object, current_col, next_col_bounds, current_row, next_row_bounds)
    rgb = 'rgb(%s, %s, %s)' % (section_avg[0], section_avg[1], section_avg[2])
    tinted_image = tint_image(tile_image, rgb)

    tinted_image_object = tinted_image.load()

    tinted_col, tinted_row = tinted_image.size

    tint_col = 0
    tint_row = 0
    try:
        for r in range(current_row, next_row_bounds):
            for c in range(current_col, next_col_bounds):
                canvas_image_object[c, r] = tinted_image_object[tint_col, tint_row]
                if tint_col >= tinted_col -1: # Next row.
                    if tint_row >= tinted_row -1:
                        # print('exited here')
                        return
                        # should end here.
                    else:
                        tint_col = 0
                        tint_row += 1
                else:
                    tint_col += 1

    except IndexError:
        print('INDEX ERROR: should end - values: col: %s tinted_col: %s, row: %s, tinted_row %s' % (tint_col, tinted_col, tint_row, tinted_row))


def memeify(meme_image, tile_image):
    canvas_image = Image.new('RGB', meme_image.size)
    canvas_image_object = canvas_image.load()
    meme_image_object = meme_image.load()

    meme_col_range, meme_row_range = meme_image.size
    tile_col_range, tile_row_range = tile_image.size

    # tile_image.show()

    # Upper bounds.
    col_divisible = math.ceil(meme_col_range/tile_col_range)
    row_divisible = math.ceil(meme_row_range/tile_row_range)

    for row in range(row_divisible):

        for col in range(col_divisible):

            cur_col = col * tile_col_range
            cur_row = row * tile_row_range
            next_col_bounds = (col + 1) * tile_col_range
            next_row_bounds = (row + 1) * tile_row_range
            # Write a single image
            write_to_meme_image(canvas_image_object, meme_image, meme_image_object, tile_image, meme_col_range, meme_row_range,
                            cur_col, next_col_bounds, cur_row, next_row_bounds)
    return canvas_image




if __name__ == "__main__":
    # Should run in download_path/venv
    # print(os.getcwd())

    # meme,image = get_meme_image_from_url('http://i0.kym-cdn.com/entries/icons/original/000/011/220/24219235.jpg')
    # Note: For unihack winning meme scale of 20 works best.
    meme_image = Image.open('../images/meme.jpg')
    scaled_meme_image = resize_image(meme_image, 25)

    tile_image = Image.open('../images/tile.jpg')
    # tile_image = tile_image.convert("RGBA")  #convert to RGBA
    # tile_image.putalpha(180) # Add opacity

    scaled_tile_image = resize_image(tile_image, 0.25)

    new_canvas_image_object = memeify(scaled_meme_image, scaled_tile_image)
    new_canvas_image_object.show()
    new_canvas_image_object.save("../images/output.jpg", "JPEG", optimize=True, quality=95)




