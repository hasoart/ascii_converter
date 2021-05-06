import tkinter as tk
import tkinter.filedialog
import tkinter.colorchooser

import re
from functools import partial

try:
    from Program_Files import styles

    styles_def = True
except:
    styles_def = False


class Disabled:
    pass


class Entry:
    def __init__(self, master, row_color=None, label_text='', default_value='', label_width=None, dtype='i++',
                 auto=False, entry_width=None, container_color=None, container_bd=None, font=None, entry_bg=None,
                 font_color=None, label_height=None, state='normal'):

        if re.match(r'^[if](\+\+|--|\+|-)$', dtype):
            self.dtype = dtype
            self.dmode = 'sign'
        elif re.match(r'^[if][(\[][+-]?([0-9]*[.])?[0-9]+:[+-]?([0-9]*[.])?[0-9]+[)\]]$', dtype):
            self.dtype = dtype
            self.dmode = 'region'
        elif dtype == 'str':
            self.dtype = 'str'
            self.dmode = 'str'
        else:
            raise TypeError("Invalid dtype")

        self.name = label_text
        self.auto = auto
        self.state = state

        if styles_def:
            if label_width is None:
                label_width = styles.label_width
            if label_height is None:
                label_height = styles.label_height
            if entry_width is None:
                entry_width = styles.entry_width
            if container_bd is None:
                container_bd = styles.container_bd
            if font is None:
                font = styles.font
            if entry_bg is None:
                entry_bg = styles.entry_bg
            if font_color is None:
                font_color = styles.entry_font_color
        else:
            if label_width is None:
                label_width = 100
            if label_height is None:
                label_height = 40
            if entry_width is None:
                entry_width = 100
            if container_bd is None:
                container_bd = 0
            if font is None:
                font = ('', 10)
            if entry_bg is None:
                entry_bg = '#ffffff'
            if font_color is None:
                font_color = '#000000'

        if row_color is None:
            row_color = '#ffffff'

        if container_color is None:
            container_color = row_color

        self.container = tk.Frame(master, bg=container_color, bd=container_bd)
        self.label_frame = tk.Frame(self.container, bg=row_color, width=label_width, height=label_height)
        self.label_frame.pack_propagate(0)
        self.label = tk.Label(self.label_frame, bg=row_color, text=label_text, fg=font_color, font=font)
        self.label.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.BOTH, padx=3, pady=2)
        self.label_frame.pack(side=tk.LEFT)

        self.entry_frame = tk.Frame(self.container, width=entry_width, height=label_height, bg=row_color)
        self.entry_frame.pack_propagate(0)
        self.entry = tk.Entry(self.entry_frame, bg=entry_bg, font=font, fg=font_color, width=entry_width)
        self.entry.insert(tk.END, default_value)
        self.entry.configure(state=state)
        self.entry.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=3, pady=2)

        self.entry_frame.pack(side=tk.LEFT)

        self.container.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def toggle_state(self):
        if self.state == 'normal':
            self.state = 'disabled'
            self.entry.configure(state=self.state)
        else:
            self.state = 'normal'
            self.entry.configure(state=self.state)

    def set_state(self, state):
        self.entry.configure(state=state)
        self.state = state

    def get(self):
        if self.state == 'disabled':
            return False, Disabled

        data = self.entry.get()
        if self.dtype == 'str':
            return False, data

        data = data.strip()
        if self.auto and data.lower() == 'auto':
            return False, 'auto'

        if self.dmode == 'sign':
            if re.match(r'^.\+$', self.dtype):
                sign = 'non-negative'
            elif re.match(r'^.\+\+$', self.dtype):
                sign = 'positive'
            elif re.match(r'^.-$', self.dtype):
                sign = 'non=positive'
            else:
                sign = 'negative'

            if self.dtype[0] == 'i':
                dtype = 'integer'
                try:
                    data = int(data)
                except:
                    return True, f'{self.name} must be a {sign} {dtype} number.'
            else:
                dtype = 'real'
                try:
                    data = float(data)
                except:
                    return True, f'{self.name} must be a {sign} {dtype} number.'

            error = (True, f'{self.name} must be a {sign} {dtype} number.')
            if sign == 'positive':
                if data <= 0:
                    return error
            elif sign == 'non-negative':
                if data < 0:
                    return error
            elif sign == 'negative':
                if data >= 0:
                    return error
            else:
                if data > 0:
                    return error

            return False, data

        if self.dmode == 'region':

            region = self.dtype[1:]
            left, right = region.split(':')
            left_par = left[0]
            right_par = right[-1]
            a = left[1:]
            b = right[:-1]
            a = float(a)
            b = float(b)
            if self.dtype[0] == 'i':
                dtype = 'integer'
                try:
                    data = int(data)
                except:
                    return True, f'{self.name} must be a {dtype} number from region {region}.'
            else:
                dtype = 'real'
                try:
                    data = float(data)
                except:
                    return True, f'{self.name} must be a {dtype} number from region {region}.'

            error = (True, f'{self.name} must be a {dtype} number from region {region}.')
            if left_par == '(':
                if data <= a:
                    return error
            else:
                if data < a:
                    return error

            if right_par == ')':
                if data >= b:
                    return error
            else:
                if data > b:
                    return error

            return False, data

    def destroy(self):
        self.label.destroy()
        self.entry.destroy()
        self.label_frame.destroy()
        self.entry_frame.destroy()
        self.container.pack_forget()
        self.container.destroy()


class FileDialog:
    def __init__(self, master, row_color='#aaaaaa', button_text='Choose file', initial_dir='', label_width=None,
                 label_height=None, entry_width=None, container_color=None, container_bd=None, font=None, entry_bg=None,
                 button_color=None, button_font_color=None):

        self.file_path = ''
        self.initial_dir = initial_dir

        if styles_def:
            if label_width is None:
                label_width = styles.label_width
            if label_height is None:
                label_height = styles.label_height
            if entry_width is None:
                entry_width = styles.entry_width
            if container_bd is None:
                container_bd = styles.container_bd
            if font is None:
                font = styles.font
            if entry_bg is None:
                entry_bg = styles.entry_bg
            if button_color is None:
                button_color = styles.button_color
            if button_font_color is None:
                button_font_color = styles.button_font_color
        else:
            if label_width is None:
                label_width = 100
            if label_height is None:
                label_height = 40
            if entry_width is None:
                entry_width = 100
            if container_bd is None:
                container_bd = 0
            if font is None:
                font = ('', 10)
            if entry_bg is None:
                entry_bg = '#ffffff'
            if button_color is None:
                button_color = '#aaaaaa'
            if button_font_color is None:
                button_font_color = '#000000'

        if row_color is None:
            row_color = '#ffffff'

        if container_color is None:
            container_color = row_color

        self.container = tk.Frame(master, bg=container_color, bd=container_bd)
        self.file_label_frame = tk.Frame(self.container, bg=row_color, width=entry_width, height=label_height)
        self.file_label_frame.pack_propagate(0)
        self.file_label = tk.Label(self.file_label_frame, bg=entry_bg, text='File not choosed', font=font, fg='#000000',
                                   width=entry_width, height=label_height, bd=1, relief="groove")
        self.file_label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=3, pady=2)
        self.file_label_frame.pack(side=tk.RIGHT)

        self.file_button_frame = tk.Frame(self.container, bg=row_color, width=label_width, height=label_height)
        self.file_button_frame.pack_propagate(0)
        self.file_button = tk.Button(self.file_button_frame, text=button_text, font=font, bg=button_color,
                                     fg=button_font_color, activebackground=button_color,
                                     activeforeground=button_font_color, command=self._get_file_path)
        self.file_button.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=3, pady=2)
        self.file_button_frame.pack(side=tk.RIGHT)

        self.container.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def _get_file_path(self):
        file_path = tk.filedialog.askopenfilename(initialdir=self.initial_dir, title='Select a Video File',
                                                  filetypes=(('All files', '*.*'),))

        if file_path == '':
            return
        else:
            file_name = file_path[file_path.rindex('/') + 1:]
            self.file_label.configure(text=file_name)
            self.file_path = file_path

    def get(self):
        if self.file_path == '':
            return True, 'File not choosed.'
        else:
            return False, self.file_path

    def destroy(self):
        self.file_label.destroy()
        self.file_button.destroy()
        self.file_label_frame.destroy()
        self.file_button_frame.destroy()
        self.container.pack_forget()
        self.container.destroy()


class FolderDialog:
    def __init__(self, master, row_color='#aaaaaa', button_text='Choose file', initial_dir='', label_width=None,
                 label_height=None, entry_width=None, container_color=None, container_bd=None, font=None, entry_bg=None,
                 button_color=None, button_font_color=None):

        self.folder_path = ''
        self.initial_dir = initial_dir

        if styles_def:
            if label_width is None:
                label_width = styles.label_width
            if label_height is None:
                label_height = styles.label_height
            if entry_width is None:
                entry_width = styles.entry_width
            if container_bd is None:
                container_bd = styles.container_bd
            if font is None:
                font = styles.font
            if entry_bg is None:
                entry_bg = styles.entry_bg
            if button_color is None:
                button_color = styles.button_color
            if button_font_color is None:
                button_font_color = styles.button_font_color
        else:
            if label_width is None:
                label_width = 100
            if label_height is None:
                label_height = 40
            if entry_width is None:
                entry_width = 100
            if container_bd is None:
                container_bd = 0
            if font is None:
                font = ('', 10)
            if entry_bg is None:
                entry_bg = '#ffffff'
            if button_color is None:
                button_color = '#aaaaaa'
            if button_font_color is None:
                button_font_color = '#000000'

        if row_color is None:
            row_color = '#ffffff'

        if container_color is None:
            container_color = row_color

        self.container = tk.Frame(master, bg=container_color, bd=container_bd)
        self.file_label_frame = tk.Frame(self.container, bg=row_color, width=entry_width, height=label_height)
        self.file_label_frame.pack_propagate(0)
        self.file_label = tk.Label(self.file_label_frame, bg=entry_bg, text='Directory not choosed', font=font,
                                   fg='#000000', width=entry_width, height=label_height, bd=1, relief="groove")
        self.file_label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=3, pady=2)
        self.file_label_frame.pack(side=tk.RIGHT)

        self.file_button_frame = tk.Frame(self.container, bg=row_color, width=label_width, height=label_height)
        self.file_button_frame.pack_propagate(0)
        self.file_button = tk.Button(self.file_button_frame, text=button_text, font=font, bg=button_color,
                                     fg=button_font_color, activebackground=button_color,
                                     activeforeground=button_font_color, command=self._get_file_path)
        self.file_button.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=3, pady=2)
        self.file_button_frame.pack(side=tk.RIGHT)

        self.container.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def _get_file_path(self):
        folder_path = tk.filedialog.askdirectory(initialdir=self.initial_dir, title='Select a the folder', )

        if folder_path == '':
            return
        else:
            folder_name = folder_path.split('/')[-1]
            self.file_label.configure(text=folder_name)
            self.folder_path = folder_path

    def get(self):
        if self.folder_path == '':
            return True, 'Directory not choosed.'
        else:
            return False, self.folder_path

    def destroy(self):
        self.file_label.destroy()
        self.file_button.destroy()
        self.file_label_frame.destroy()
        self.file_button_frame.destroy()
        self.container.pack_forget()
        self.container.destroy()


class Button:
    def __init__(self, master, row_color='#aaaaaa', button_text='Run', button_height=None, container_color=None,
                 container_bd=None, font=None, button_color=None, button_font_color=None, command=None):

        if styles_def:
            if button_height is None:
                button_height = styles.button_height
            if container_bd is None:
                container_bd = styles.container_bd
            if font is None:
                font = styles.font
            if button_color is None:
                button_color = styles.button_color
            if button_font_color is None:
                button_font_color = styles.button_font_color
        else:
            if button_height is None:
                button_height = 40
            if container_bd is None:
                container_bd = 0
            if font is None:
                font = ('', 10)
            if button_color is None:
                button_color = '#aaaaaa'
            if button_font_color is None:
                button_font_color = '#000000'

        if container_color is None:
            container_color = row_color

        self.container = tk.Frame(master, bg=container_color, bd=container_bd)
        self.run_button_frame = tk.Frame(self.container, bg=row_color, width=200, height=button_height)
        self.run_button_frame.pack_propagate(0)
        self.run_button = tk.Button(self.run_button_frame, text=button_text, bg=button_color, fg=button_font_color,
                                    font=font, activebackground=button_color, activeforeground=button_font_color,
                                    command=command)
        self.run_button.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)
        self.run_button_frame.pack(side=tk.TOP)
        self.container.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def destroy(self):
        self.run_button.destroy()
        self.run_button_frame.destroy()
        self.container.pack_forget()
        self.container.destroy()


class ColorChooser:
    def __init__(self, master, row_color=None, label_text='', default_value='', label_width=None,
                 label_height=None, entry_width=None, container_color=None, container_bd=None, font=None, entry_bg=None,
                 font_color=None, button_color=None, button_font_color=None):

        self.label_text = label_text

        if styles_def:
            if label_width is None:
                label_width = styles.label_width
            if label_height is None:
                label_height = styles.label_height
            if entry_width is None:
                entry_width = styles.entry_width
            if container_bd is None:
                container_bd = styles.container_bd
            if font is None:
                font = styles.font
            if entry_bg is None:
                entry_bg = styles.entry_bg
            if font_color is None:
                font_color = styles.entry_font_color
            if button_color is None:
                button_color = styles.button_color
            if button_font_color is None:
                button_font_color = styles.button_font_color
        else:
            if label_width is None:
                label_width = 100
            if label_height is None:
                label_height = 40
            if entry_width is None:
                entry_width = 100
            if container_bd is None:
                container_bd = 0
            if font is None:
                font = ('', 10)
            if entry_bg is None:
                entry_bg = '#ffffff'
            if font_color is None:
                font_color = '#000000'
            if button_color is None:
                button_color = '#aaaaaa'
            if button_font_color is None:
                button_font_color = '#000000'

        if row_color is None:
            row_color = '#ffffff'

        if container_color is None:
            container_color = row_color

        self.container = tk.Frame(master, bg=container_color, bd=container_bd)

        self.label_frame = tk.Frame(self.container, bg=row_color, width=label_width, height=label_height)
        self.label_frame.pack_propagate(0)
        self.label = tk.Label(self.label_frame, bg=row_color, text=label_text, fg=font_color, font=font)
        self.label.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.BOTH, padx=3, pady=2)
        self.label_frame.pack(side=tk.LEFT)

        self.entry_frame = tk.Frame(self.container, width=entry_width - label_height - 3, height=label_height,
                                    bg=row_color)
        self.entry_frame.pack_propagate(0)
        self.entry = tk.Entry(self.entry_frame, bg=entry_bg, font=font, fg=font_color, width=entry_width)
        self.entry.insert(0, default_value)
        self.entry.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=3, pady=2)
        self.entry_frame.pack(side=tk.LEFT)

        self.button_frame = tk.Frame(self.container, width=label_height, height=label_height, bg=row_color)
        self.button_frame.pack_propagate(0)
        self.button = tk.Button(self.button_frame, height=label_height, width=label_height, text='Pick',
                                bg=button_color,
                                activebackground=button_color, activeforeground=button_font_color, fg=button_font_color,
                                font=font, command=self.get_color)
        self.button.pack(side=tk.LEFT)
        self.button_frame.pack(side=tk.LEFT)

        self.container.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def get_color(self):
        color = tk.colorchooser.askcolor(title='Choose color')

        if color[1] is not None:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, color[1])

    def get(self):
        color = self.entry.get().strip()

        if re.match(r'^#[0-9a-fA-F]{6}$', color):
            return False, color
        else:
            return True, f'{self.label_text} must be a valid color in #rrggbb format.'

    def destroy(self):
        self.entry.destroy()
        self.label.destroy()
        self.button.destroy()
        self.entry_frame.destroy()
        self.button_frame.destroy()
        self.label_frame.destroy()
        self.container.pack_forget()
        self.container.destroy()


class RadioButton:
    def __init__(self, master, row_color=None, options=None, options_labels=None, default_value=None, button_width=None,
                 command=None, height=None, container_bd=None, font=None, button_font_color=None):

        self.mode = tk.StringVar(master)
        self.mode.set(options[0])

        def button_command(x):
            self.mode.set(x)
            if command is not None:
                command(x)

        if styles_def:
            if button_width is None:
                button_width = styles.radiobutton_width
            if height is None:
                height = styles.label_height
            if container_bd is None:
                container_bd = styles.container_bd
            if font is None:
                font = styles.font
            if button_font_color is None:
                button_font_color = styles.radiobutton_font_color
        else:
            if button_width is None:
                button_width = 80
            if height is None:
                height = 40
            if container_bd is None:
                container_bd = 0
            if font is None:
                font = ('', 10)
            if button_font_color is None:
                button_font_color = '#000000'

        if row_color is None:
            row_color = '#aaaaaa'

        if options_labels is None:
            options_labels = options

        self.row_container = tk.Frame(master, bg=row_color, bd=container_bd)
        self.container = tk.Frame(self.row_container, bg=row_color)
        buttons = []
        for col, option in enumerate(options):
            self.container.columnconfigure(col, weight=1, uniform='uniform')
            button_frame = tk.Frame(self.container, width=button_width, height=height, bg=row_color)
            button_frame.pack_propagate(0)
            button = tk.Radiobutton(button_frame, text=options_labels[col], variable=self.mode, value=option,
                                    font=font, fg=button_font_color, activeforeground=button_font_color,
                                    bg=row_color, activebackground=row_color, highlightthickness=0, bd=0,
                                    command=partial(button_command, option))
            button.pack(side=tk.LEFT)
            buttons.append(button)
            button_frame.grid(row=0, column=col)
        if isinstance(default_value, int):
            buttons[default_value].select()
        else:
            buttons[options.index(default_value)].select()
        self.container.pack()
        self.row_container.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def get(self):
        return False, self.mode.get()
