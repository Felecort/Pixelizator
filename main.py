
# PixelArtCode
import cv2
from tkinter import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from time import time
import numpy as np


# Creating a dialog box for selecting a file
def selecting_file():
    Tk().withdraw()
    file_name = askopenfilename()
    return file_name


# Saving an image with adding "EDIT" at the end of the file to the source folder
def save_image(image, image_name):
    symbol_index = image_name.rfind('.')
    image_name = image_name[:symbol_index] + "_EDIT" + image_name[symbol_index:]
    cv2.imwrite(image_name, image)


# Drawing an image on the screen
def draw_image(image, image_name, pixel_size):
    cv2.imshow(f"PixelArt, size = {pixel_size}", image)
    key = cv2.waitKey(0)
    if key == 115:
        save_image(image, image_name)
    cv2.destroyAllWindows()


# Converting an image to pixel art
def conversion_to_pixel(image, pixel_size=15):
    width = int(image.shape[1])
    height = int(image.shape[0])
    # resolution of the final image
    pixel_height = int((height - pixel_size) / pixel_size) + 1
    pixel_width = int((width - pixel_size) / pixel_size) + 1
    half_pixel_size = int(pixel_size / 2)
    x_out = 0
    y_out = 0
    out_image = np.zeros((pixel_height, pixel_width, 3), dtype=np.uint8)
    for y in range(0, height - pixel_size + 1, pixel_size):
        for x in range(0, width - pixel_size + 1, pixel_size):
            pixel_color = image[y + half_pixel_size, x + half_pixel_size]
            out_image[y_out, x_out] = pixel_color
            x_out += 1
        y_out += 1
        x_out = 0
    out_image = cv2.resize(out_image, (width, height))
    return out_image


# Pixelation of the video stream
def pixel_video(video, pixel_size):
    while True:
        ret, frame = video.read()
        key = cv2.waitKey(1)
        if not ret or (key & 0xFF in [27, 32, 113]):
            break
        image = conversion_to_pixel(frame, pixel_size)
        cv2.imshow("frame", image)
    video.release()
    cv2.destroyAllWindows()


# Pixel art of a single image
def image_pixel_art():
    pixel_size = int(entry_pixel_size.get())
    image_name = selecting_file()
    if image_name == '':
        print('missing the input image')
        return 0
    image = cv2.imread(image_name)
    pixel_img = conversion_to_pixel(image, pixel_size)
    draw_image(pixel_img, image_name, pixel_size)


# Pixelation of video and output to the screen
def video_pixel_art():
    pixel_size = int(entry_pixel_size.get())
    video_name = selecting_file()
    if video_name == '':
        print('missing the input video')
        return 0
    elif video_name[-3:] != "mp4":
        print("only mp4 videos are supported")
        return 0
    start = time()

    video = cv2.VideoCapture(video_name)
    fps = video.get(cv2.CAP_PROP_FPS)
    ret, frame = video.read()
    height = (int((int(frame.shape[0]) - pixel_size) / pixel_size) + 1) * pixel_size
    width = (int((int(frame.shape[1]) - pixel_size) / pixel_size) + 1) * pixel_size

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    symbol_index = video_name.rfind('.')
    video_name = video_name[:symbol_index] + "_EDIT.mp4"
    out = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    while True:
        ret, frame = video.read()
        if not ret:
            break
        image = conversion_to_pixel(frame, pixel_size)
        out.write(image)
    video.release()
    out.release()
    print(time() - start)
    cv2.destroyAllWindows()


# Pixelate webcam video and display it on the screen
def webcam_pixel_art():
    pixel_size = int(entry_pixel_size.get())
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    pixel_video(video, pixel_size)


# The formation of the main window
window = Tk()

icon = PhotoImage(file="data/icon.png")
window.iconphoto(False, icon)
window.geometry("700x400+300+350")
window.resizable(False, False)
window.title("Python Art by FriLDD")
window.config(bg="#33cccc")

# Text on the main window
lbl = Label(window,
            text="Enter the pixel size",
            font=("Arial", 20, "bold"),
            bg="#33cccc"
            )
lbl.place(x=20, y=20)

# Text input window options
entry_pixel_size = Entry(window,
                         width=10,
                         font=("Arial", 12, "bold"))
entry_pixel_size.place(x=20, y=60)
entry_pixel_size.insert(0, "20")
entry_pixel_size.focus()

# Calling functions based on clicks
# state.Tk=DISABLED
image_button = Button(window, text="Image", command=image_pixel_art,
                      activebackground="#E0E0E0",
                      font=("Arial", 12),
                      width=10
                      )
image_button.place(x=20, y=100)
video_button = Button(window, text="Video", command=video_pixel_art,
                      activebackground="#E0E0E0",
                      font=("Arial", 12),
                      width=10
                      )
video_button.place(x=20, y=140)
webcam_button = Button(window, text="Webcam", command=webcam_pixel_art,
                       activebackground="#E0E0E0",
                       font=("Arial", 12),
                       width=10
                       )
webcam_button.place(x=20, y=180)

# Exit
exit_button = Button(window, text="Exit",
                     command=lambda: exit(),
                     activebackground="#E0E0E0",
                     font=("Arial", 12),
                     width=10
                     )
exit_button.place(x=20, y=350)

# Starting an infinite loop
window.mainloop()
