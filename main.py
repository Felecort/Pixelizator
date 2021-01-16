
# PixelArtCode
import cv2
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def save_image(image, image_name):
    symbol_index = image_name.rfind('.')
    image_name = image_name[:symbol_index] + "_EDIT" + image_name[symbol_index:]
    cv2.imwrite(image_name, image)


def pixel_image(image_name, pixel_size=15):
    if image_name == '':
        print('missing the input image')
        return -1
    start = time.time()
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
    cv2.imshow("PixelArt", cropped_image)
    print(1 / (time.time() - start), 'fps')
    key = cv2.waitKey(0)
    if key == 115:
        save_image(image, image_name)
    cv2.destroyAllWindows()


# creating a dialog box for selecting a file
Tk().withdraw()
filename = askopenfilename()

PIXEL_SIZE = 10
pixel_image(filename, PIXEL_SIZE)
