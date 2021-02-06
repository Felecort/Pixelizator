
# PixelArtCode
import cv2
import numpy as np
import sys
import tkinter
from tkinter.filedialog import askopenfilename
from webbrowser import open_new
from numba import njit


# Saving an image with adding "EDIT" at the end of the file to the source folder
def save_image(image, image_name):
    symbol_index = image_name.rfind('.')
    image_name = image_name[:symbol_index] + "_EDIT" + image_name[symbol_index:]
    cv2.imwrite(image_name, image)


# Drawing an image on the screen
def draw_image(image, image_name, pixel_size):
    cv2.imshow(f"Size = {pixel_size}", image)
    key = cv2.waitKey(0)
    if key in [115, 251]:
        save_image(image, image_name)
        canvas_update_status("Изображение сохранено", 12)
        canvas_progress.update()
    cv2.destroyAllWindows()


# Creating a new image by taking one pixel of the area of the original image
# and painting over one pixel of the other
@njit(fastmath=True)
def pixelation_algorithm(image, pixel_size):
    height, width = image.shape[0:2]
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
    return out_image


# Auxiliary function: needed to call the main algorithm in acceleration mode
def conversion_to_pixel(image, pixel_size=15):
    out_image = pixelation_algorithm(image, pixel_size)
    out_image_resize = cv2.resize(out_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    return out_image_resize


# Pixel art of a single image
def image_pixel_art():
    canvas_update_rect()
    pixel_size = get_pixel_size()

    image_name = askopenfilename()
    if image_name == '':
        canvas_update_status("Изображение отсутствует", 12)
        return 0
    elif image_name[-3:] not in ["jpg", "png"]:
        canvas_update_status("Неподдерживаемый формат файла", 10)
        return 0
    image = cv2.imread(image_name)
    pixel_img = conversion_to_pixel(image, pixel_size)
    draw_image(pixel_img, image_name, pixel_size)


# Pixelation of video and output to the screen
def video_pixel_art():
    canvas_update_rect()
    pixel_size = get_pixel_size()
    video_name = askopenfilename()
    if video_name == '':
        canvas_update_status("Видео отсутствует", 12)
        return 0
    elif video_name[-3:] != "mp4":
        canvas_update_status("Неподдерживаемый формат файла", 10)
        return 0

    video = cv2.VideoCapture(video_name)
    number_of_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    count_frames = 0

    ret, frame = video.read()
    height, width = frame.shape[0:2]
    symbol_index = video_name.rfind('.')
    video_name = video_name[:symbol_index] + "_EDIT.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
    while True:
        ret, frame = video.read()
        if not ret:
            break
        progress = round(count_frames / number_of_frames * 100)
        if progress % 2 == 0:
            draw_progress(progress)
        count_frames += 1
        image = conversion_to_pixel(frame, pixel_size)
        out.write(image)
    draw_progress(100)
    canvas_progress.create_text(125, 17, text="Успешно!", font=("Arial", 12, "bold"), fill="#000000")
    video.release()
    out.release()
    cv2.destroyAllWindows()


# Pixelate webcam video and display it on the screen
def webcam_pixel_art():
    canvas_update_rect()
    pixel_size = get_pixel_size()
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    canvas_update_status("Успешно!", 12)
    while True:
        ret, frame = video.read()
        key = cv2.waitKey(1)
        if not ret or (key & 0xFF in [27, 32, 113]):
            break
        image = conversion_to_pixel(frame, pixel_size)
        cv2.imshow("frame", image)
    video.release()
    cv2.destroyAllWindows()


# Getting and processing the pixel size
def get_pixel_size():
    try:
        ps = int(entry_pixel_size.get())
        if ps < 1:
            canvas_update_status("Невозможный размер пикселизации", 10)
            return abs(ps) + 1
        else:
            return ps
    except ValueError:
        canvas_update_status("Невозможный размер пикселизации", 10)
        return 1


# GUI
# Updating the text status
def canvas_update_status(text, font_size):
    canvas_progress.update()
    canvas_progress.delete(tkinter.ALL)
    canvas_progress.create_text(125, 17,
                                text=text,
                                font=("Arial", font_size, "bold"),
                                fill="#000000"
                                )


# Updating the rectangle rendering
def canvas_update_rect():
    canvas_progress.update()
    canvas_progress.delete(tkinter.ALL)
    canvas_progress.create_rectangle(0, 0,
                                     250, 50,
                                     fill="#33cccc",
                                     width=0
                                     )


# Drawing the progress of video processing
def draw_progress(progress):
    progress *= 2.5
    canvas_progress.update()
    canvas_progress.delete(tkinter.ALL)
    canvas_progress.create_rectangle(0, 0,
                                     progress, 50,
                                     fill="#E0E0E0",
                                     width=0
                                     )
    return 0


# Start Program
# Warming up the cache
conversion_to_pixel(cv2.imread(sys.path[0] + "\\warming_up_the_cache.png"), 2)

# Preparing the file selection window
select_file_window = tkinter.Tk()
select_file_window.withdraw()

# The formation of the main window
window = tkinter.Tk()

window.geometry("700x400+300+350")
window.resizable(False, False)
window.title("Python Art by FriLDD")
window.config(bg="#33cccc")

# Text on the main window
title_label = tkinter.Label(window,
                            text="Размер пикселя:",
                            font=("Arial", 14, "bold"),
                            bg="#33cccc"
                            )
title_label.place(x=20, y=20)
title_label.update()

video_label = tkinter.Label(window,
                            text="Статус:",
                            font=("Arial", 14, "bold"),
                            bg="#33cccc"
                            )
video_label.place(x=250, y=52)

description_label = tkinter.Label(window,
                                  text="""
Для сохранения изображения нажмите "s" 

Закрыть изображение: "space" или "esc"

Обработанные видео сохраняются
в той же папке, где и оригинал
                            """,
                                  font=("Arial", 12, "bold"),
                                  bg="#33cccc",
                                  justify=tkinter.LEFT
                                  )
description_label.place(x=300, y=200)

author_label = tkinter.Label(window,
                             text="Автор приложения: FriLDD *клик*",
                             font=("Arial", 12, "bold"),
                             bg="#33cccc",
                             cursor="hand2"
                             )
author_label.place(x=300, y=360)
author_label.bind("<Button-1>", lambda x: open_new("https://github.com/FriLDD"))

# Text input window options
entry_pixel_size = tkinter.Entry(window,
                                 width=12,
                                 font=("Arial", 14))
entry_pixel_size.place(x=20, y=50)
entry_pixel_size.insert(0, "10")
entry_pixel_size.focus()
entry_pixel_size.update()

# Calling functions based on clicks
image_button = tkinter.Button(window, text="Изображение", command=image_pixel_art,
                              activebackground="#E0E0E0",
                              font=("Arial", 14),
                              width=12
                              )
image_button.place(x=20, y=100)
video_button = tkinter.Button(window, text="Видео", command=video_pixel_art,
                              activebackground="#E0E0E0",
                              font=("Arial", 14),
                              width=12
                              )
video_button.place(x=20, y=150)
webcam_button = tkinter.Button(window, text="Веб-камера", command=webcam_pixel_art,
                               activebackground="#E0E0E0",
                               font=("Arial", 14),
                               width=12
                               )
webcam_button.place(x=20, y=200)

# Exit
exit_button = tkinter.Button(window, text="Выход",
                             command=lambda: sys.exit(),
                             activebackground="#E0E0E0",
                             font=("Arial", 12),
                             width=10
                             )
exit_button.place(x=20, y=350)

# Progress bar
canvas_progress = tkinter.Canvas(window,
                                 width=248,
                                 height=30,
                                 bg="#33cccc"
                                 )
canvas_progress.place(x=330, y=50)

# Closing the app by clicking the cross
window.protocol("WM_DELETE_WINDOW", sys.exit)
# Starting an infinite loop
window.mainloop()
