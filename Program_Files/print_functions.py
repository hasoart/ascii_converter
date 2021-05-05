import tkinter as tk
import tkinter.messagebox
import tkinter.colorchooser
import tkinter.ttk as ttk

import os
import threading

import cv2
import numpy as np
import time
from ffpyplayer.player import MediaPlayer

from Program_Files import functions as fn
from Program_Files.paths import *
from Program_Files.styles import *

pixels = np.array(['  ', '..', ',,', '--', '~~', '::', ';;', '==', '!!', '**', '##', '$$', '@@'])
pixel_const = len(pixels)
pixel_factor = pixel_const / 256
pixel_size = len(pixels[0])


def set_color(entry):
    color = tk.colorchooser.askcolor(title='Choose color')

    if color[1] is not None:
        entry.delete(0, tk.END)
        entry.insert(0, color[1])


def check_settings(entry_dict, function_to_run):
    error_message = []
    settings = {}
    for entry in entry_dict:
        error, value = entry_dict[entry].get()
        if not error:
            settings[entry] = value
        else:
            error_message.append(value)

    if 'auto' == settings.get('frame_width') == settings.get('frame_height'):
        error_message.append('Frame width and Frame height can\'t be \'auto\' simultaneously.')

    # print(settings)

    if error_message:
        tk.messagebox.showerror(title='Error', message='\n'.join(error_message))
    else:
        function_to_run(**settings)


def real_time_printer(file_path, framerate, frame_height, frame_width, font_size, font_color, bg_color, volume, timeout,
                      mode, scale):
    video = cv2.VideoCapture(file_path)
    success, image = video.read()
    if not success:
        tk.messagebox.showerror(title='Error!', message='Bad file')
        return

    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if framerate == 'auto':
        framerate = video.get(cv2.CAP_PROP_FPS)

    frame_time = 1000 / framerate

    video_height = len(image)
    video_width = len(image[0])

    if mode == 'scale':
        converted_height = int(video_height // scale)
        converted_width = int(video_width // scale)
    elif mode == 'size':
        converted_height = frame_height
        converted_width = frame_width

        if converted_width == 'auto':
            converted_width = int(video_width * converted_height / video_height)
        elif converted_height == 'auto':
            converted_height = int(video_height * converted_width / video_width)
    else:
        raise ValueError('Incorrect or no conversion parameters.')

    file_name = file_path.split('/')[-1]
    canvas_title = file_name[:file_name.rindex('.')]

    def on_closing_canvas():
        video.release()
        canvas.destroy()
        audio_player.close_player()

    canvas = tk.Tk()
    canvas.title(canvas_title)
    canvas.configure(bg=bg_color)
    canvas.geometry('')

    canvas.protocol("WM_DELETE_WINDOW", on_closing_canvas)

    text_box = tk.Text(canvas, width=converted_width * pixel_size, height=converted_height,
                       bg=bg_color, bd=0, font=('courier', font_size),
                       fg=font_color)
    text_box.grid(row=0, column=0)

    frame_counter = 0

    prev_finish_time = 0.0
    cum_sum = 0.0
    audio_player: MediaPlayer

    def init():
        nonlocal audio_player

        audio_player_options = {'autoexit': True,
                                'vn': True,
                                'sn': True}

        audio_player = MediaPlayer(file_path, ff_opts=audio_player_options)
        audio_player.toggle_pause()

        def first_frame():
            audio_player.toggle_pause()
            audio_player.set_volume(volume/100)
            next_frame()

        canvas.after(max(int(timeout * 1000), 1000), first_frame)

    def next_frame():
        nonlocal frame_counter, prev_finish_time, cum_sum, image, success
        start_time = time.time()
        if not success and frame_counter != frame_count:
            raise EOFError

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, dsize=(converted_width, converted_height),
                           interpolation=cv2.INTER_CUBIC)
        char_image = pixels[(image * pixel_factor).astype(int)]

        text_box.delete(1.0, "end-1c")
        text_box.insert("end-1c", fn.join_2d_array_to_frame(char_image))
        success, image = video.read()
        frame_counter += 1

        if success:
            finish_time = time.time()
            time_difference = frame_time - (finish_time - prev_finish_time) * 1000
            cum_sum += time_difference * (frame_counter > 2)
            dt = frame_time - (finish_time - start_time) * 1000 + cum_sum
            prev_finish_time = finish_time
            if dt >= 0:
                canvas.after(int(dt), next_frame)
            else:
                print(f'Significant drift noticed. {round(cum_sum, 3)}ms.')
                canvas.after(0, next_frame)

        else:
            on_closing_canvas()

    canvas.after(0, init)
    canvas.mainloop()


def from_file_printer(file_path, framerate, font_size, font_color, bg_color, timeout):
    frame_time = 1000 / framerate

    file_path = file_path

    def on_closing_canvas():
        canvas.destroy()

    canvas = tk.Tk()
    file_name = file_path.split('/')[-1]
    canvas_title = file_name[:file_name.rindex('.')]

    canvas.title(canvas_title)
    canvas.configure(bg=bg_color)
    canvas.geometry('')

    canvas.protocol('WM_DELETE_WINDOW', on_closing_canvas)

    if file_path[-4:] == '.txt':
        with open(file_path, 'r') as f:
            frame_list = f.read().split('|\n')

        test_frame = frame_list[0].split('\n')
        frame_width = len(test_frame[0])
        frame_height = len(test_frame) - 1

        text_box = tk.Text(canvas, width=frame_width, height=frame_height, bg=bg_color, bd=0,
                           font=('courier', font_size), fg=font_color)
        text_box.grid(row=0, column=0)

        frame_counter = 0
        frame_count = len(frame_list)

        prev_finish_time = 0.0
        cum_sum = 0

        def next_frame():
            nonlocal prev_finish_time, cum_sum, frame_counter
            start_time = time.time()
            text_box.delete(1.0, "end-1c")
            text_box.insert("end-1c", frame_list[frame_counter])
            frame_counter += 1
            if frame_counter != frame_count:
                finish_time = time.time()
                time_difference = frame_time - (finish_time - prev_finish_time) * 1000
                cum_sum += time_difference * (frame_counter > 2)
                dt = frame_time - (finish_time - start_time) * 1000 + cum_sum
                prev_finish_time = finish_time
                if dt >= 0:
                    canvas.after(int(dt), next_frame)
                else:
                    print(f'Significant drift noticed. {round(cum_sum, 3)}ms.')
                    canvas.after(0, next_frame)
            else:
                on_closing_canvas()

        canvas.after(int(timeout * 1000), next_frame)
        canvas.mainloop()
    else:
        tk.messagebox.showerror(title='Error!', message='File not supported')
        on_closing_canvas()
        return


def convert_to_frames(master, file_path, mode, scale, frame_height, frame_width, row_color):
    video_name = file_path.split('/')[-1]

    frame_pack_path = extracted_frames_path + video_name[:video_name.rindex('.')] + '/'

    if video_name[:video_name.rindex('.')] not in os.listdir(extracted_frames_path):
        os.makedirs(frame_pack_path)

    vidcap = cv2.VideoCapture(file_path)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    name_len = len(str(length))
    success, image = vidcap.read()

    pb_style = ttk.Style()
    pb_style.theme_use('clam')
    pb_style.configure('pbstyle.Horizontal.TProgressbar', troughcolor=row_color, background='#3dff7e',
                       darkcolor='#3dff7e', lightcolor='#3dff7e', bordercolor=row_color)

    video_width = len(image[0])
    video_height = len(image)

    if mode == 'scale':
        converted_width = int(video_width // scale)
        converted_height = int(video_height // scale)
    else:
        if frame_height == 'auto':
            converted_width = frame_width
            converted_height = int(video_height * frame_width / video_width)
        elif frame_width == 'auto':
            converted_height = frame_height
            converted_width = int(video_width * frame_height / video_height)
        else:
            converted_height = frame_height
            converted_width = frame_width

    def convert():
        pb_container = tk.Frame(master, bg=row_color, bd=container_bd)
        pb = ttk.Progressbar(pb_container, style='pbstyle.Horizontal.TProgressbar',
                             length=entry_width + label_width, mode='determinate', maximum=length)
        pb.pack(side=tk.TOP)
        pb_container.pack(side=tk.TOP)

        nonlocal image, success
        for count in range(1, length + 1):
            png_name = frame_pack_path + f'/{"0" * (name_len - len(str(count)))}{count}.png'
            image = cv2.resize(image, dsize=(converted_width, converted_height), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(png_name, image)
            success, image = vidcap.read()
            pb['value'] += 1

            if not success and count == length:
                pb.stop()
                pb.destroy()
                pb_container.destroy()
                tk.messagebox.showinfo(title='Success!', message='Extraction finished!')
                break
            elif not success and count != length:
                pb.stop()
                pb.destroy()
                pb_container.destroy()
                tk.messagebox.showerror(title='Error!', message='Extraction failed due to unknown reasons!')
                break

    threading.Thread(target=convert).start()


def convert_to_ascii(master, directory, mode, scale, frame_height, frame_width, row_color):
    folder_name = directory.split('/')[-1]

    frames = os.listdir(directory)

    pb_style = ttk.Style()
    pb_style.theme_use('clam')
    pb_style.configure('pbstyle.Horizontal.TProgressbar', troughcolor=row_color, background='#3dff7e',
                       darkcolor='#3dff7e', lightcolor='#3dff7e', bordercolor=row_color)

    def convert():
        pb_container = tk.Frame(master, bg=row_color, bd=container_bd)
        pb = ttk.Progressbar(pb_container, style='pbstyle.Horizontal.TProgressbar',
                             length=entry_width + label_width, mode='determinate', maximum=len(frames))
        pb.pack(side=tk.TOP)
        pb_container.pack(side=tk.TOP)

        with open(result_files_path + folder_name + '.txt', 'w') as f:
            for frame in frames:
                frame_path = directory + '/' + frame

                image = cv2.imread(frame_path, 0)

                height = len(image)
                width = len(image[0])

                if mode == 'scale':
                    m = int(height // scale)
                    n = int(width // scale)
                else:
                    if frame_width == 'auto':
                        m = frame_height
                        n = int(width * m / height)
                    elif frame_height == 'auto':
                        n = frame_width
                        m = int(height * n / width)
                    else:
                        m = frame_height
                        n = frame_width

                image = cv2.resize(image, dsize=(n, m), interpolation=cv2.INTER_CUBIC)
                f.write(fn.join_2d_array(pixels[(image * pixel_factor).astype(int)]))
                pb['value'] += 1

            pb.stop()
            pb.destroy()
            pb_container.destroy()
            tk.messagebox.showinfo(title='Success!', message='Conversion finished!')

    threading.Thread(target=convert).start()
