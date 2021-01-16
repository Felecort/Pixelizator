
# PixelArtCode

import cv2
import time


def pixel_image(image_name, pixel_size=15):
    start = time.time()
    image = cv2.imread("img/" + image_name)
    width = int(image.shape[1])
    height = int(image.shape[0])
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
    cv2.waitKey(0)
    cv2.destroyAllWindows()


IMAGE_NAME = "02.jpg"
PIXEL_SIZE = 10

pixel_image(IMAGE_NAME, PIXEL_SIZE)
