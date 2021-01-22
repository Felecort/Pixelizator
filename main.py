
# PixelArtCode
import cv2
from tkinter import *
from tkinter.filedialog import askopenfilename
import numpy as np
import sys
from webbrowser import open_new


# Creating a dialog box for selecting a file
def selecting_file():
    Tk().withdraw()
    file_name = askopenfilename()
    return file_name


def canvas_update_status(text, font_size):
    canvas_progress.update()
    canvas_progress.create_text(125, 17,
                                text=text,
                                font=("Arial", font_size, "bold"),
                                fill="#000000"
                                )


def canvas_update_rect():
    canvas_progress.update()
    canvas_progress.create_rectangle(0, 0,
                                     250, 50,
                                     fill="#33cccc",
                                     width=0
                                     )


# Drawing the progress of video processing
def draw_progress(progress):
    progress *= 2.5
    canvas_progress.update()
    canvas_progress.delete(ALL)
    canvas_progress.create_rectangle(0, 0,
                                     progress, 50,
                                     fill="#E0E0E0",
                                     width=0
                                     )
    return 0


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


# Converting an image to pixel art
def conversion_to_pixel(image, pixel_size=15):
    width = int(image.shape[1])
    height = int(image.shape[0])
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
    out_image = cv2.resize(out_image, (width, height), interpolation=cv2.INTER_NEAREST)
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
    canvas_update_rect()
    pixel_size = int(entry_pixel_size.get())
    image_name = selecting_file()
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
    pixel_size = int(entry_pixel_size.get())
    video_name = selecting_file()
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
    width = int(frame.shape[1])
    height = int(frame.shape[0])

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
    canvas_update_status("Успешно!", 12)
    video.release()
    out.release()
    cv2.destroyAllWindows()


# Pixelate webcam video and display it on the screen
def webcam_pixel_art():
    canvas_update_rect()
    pixel_size = int(entry_pixel_size.get())
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    canvas_update_status("Успешно!", 12)
    pixel_video(video, pixel_size)


# The formation of the main window
window = Tk()

window.geometry("700x400+300+350")
window.resizable(False, False)
window.title("Python Art by FriLDD")
window.config(bg="#33cccc")

# Text on the main window
title_label = Label(window,
                    text="Размер пикселя:",
                    font=("Arial", 14, "bold"),
                    bg="#33cccc"
                    )
title_label.place(x=20, y=20)
title_label.update()

video_label = Label(window,
                    text="Статус:",
                    font=("Arial", 14, "bold"),
                    bg="#33cccc"
                    )
video_label.place(x=250, y=52)

description_label = Label(window,
                          text="""
Для сохранения изображения нажмите "s" 

Закрыть изображение: "space" или "esc"

Обработанные видео сохраняются
в той же папке, где и оригинал
                            """,
                          font=("Arial", 12, "bold"),
                          bg="#33cccc",
                          justify=LEFT
                          )
description_label.place(x=300, y=200)

author_label = Label(window,
                     text="Автор приложения: https://github.com/FriLDD",
                     font=("Arial", 12, "bold"),
                     bg="#33cccc",
                     cursor="hand2"
                     )
author_label.place(x=300, y=360)
author_label.bind("<Button-1>", lambda x: open_new("https://github.com/FriLDD"))

# Text input window options
entry_pixel_size = Entry(window,
                         width=12,
                         font=("Arial", 14))
entry_pixel_size.place(x=20, y=50)
entry_pixel_size.insert(0, "10")
entry_pixel_size.focus()
entry_pixel_size.update()

# Calling functions based on clicks
# state.Tk=DISABLED
image_button = Button(window, text="Изображение", command=image_pixel_art,
                      activebackground="#E0E0E0",
                      font=("Arial", 14),
                      width=12
                      )
image_button.place(x=20, y=100)
video_button = Button(window, text="Видео", command=video_pixel_art,
                      activebackground="#E0E0E0",
                      font=("Arial", 14),
                      width=12
                      )
video_button.place(x=20, y=150)
webcam_button = Button(window, text="Веб-камера", command=webcam_pixel_art,
                       activebackground="#E0E0E0",
                       font=("Arial", 14),
                       width=12
                       )
webcam_button.place(x=20, y=200)

# Exit
exit_button = Button(window, text="Выход",
                     command=lambda: sys.exit(),
                     activebackground="#E0E0E0",
                     font=("Arial", 12),
                     width=10
                     )
exit_button.place(x=20, y=350)

canvas_progress = Canvas(window,
                         width=248,
                         height=30,
                         bg="#33cccc"
                         )
canvas_progress.place(x=330, y=50)

# Starting an infinite loop
window.mainloop()
