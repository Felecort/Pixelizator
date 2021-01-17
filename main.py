# PixelArtCode
import cv2
from time import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def save_image(image, image_name):
    symbol_index = image_name.rfind('.')
    image_name = image_name[:symbol_index] + "_EDIT" + image_name[symbol_index:]
    cv2.imwrite(image_name, image)


def draw_image(image, image_name, pixel_size):
    cv2.imshow(f"PixelArt, size = {pixel_size}", image)
    key = cv2.waitKey(0)
    if key == 115:
        save_image(image, image_name)
    cv2.destroyAllWindows()


def conversion_to_pixel(image_name, pixel_size=15):
    image = cv2.imread(image_name)
    width = int(image.shape[1])
    height = int(image.shape[0])
    # resolution of the final image
    pixel_height = int((height - pixel_size) / pixel_size) + 1
    pixel_width = int((width - pixel_size) / pixel_size) + 1
    half_pixel_size = int(pixel_size / 2)
    for y in range(0, height - pixel_size + 1, pixel_size):
        for x in range(0, width - pixel_size + 1, pixel_size):
            pixel_color = image[y + half_pixel_size, x + half_pixel_size]
            image[y:y + pixel_size, x:x + pixel_size] = pixel_color
    cropped_image = image[0:pixel_height * pixel_size, 0:pixel_width * pixel_size]
    return cropped_image


def pixel_image(image_name, pixel_size=15):
    image = conversion_to_pixel(image_name, pixel_size)
    draw_image(image, image_name, pixel_size)


# creating a dialog box for selecting a file
Tk().withdraw()
FILE_NAME = askopenfilename()
if FILE_NAME == '':
    print('missing the input image')
    exit()

PIXEL_SIZE = 10
pixel_image(FILE_NAME, PIXEL_SIZE)
# video_pixel_art(FILE_NAME, PIXEL_SIZE)