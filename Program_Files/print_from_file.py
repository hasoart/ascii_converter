import tkinter as tk

from functools import partial
from itertools import cycle

from Program_Files import functions as fn
from Program_Files import print_functions as pf
from Program_Files import custom_widgets as cw

from Program_Files.styles import *
from Program_Files.paths import *


def main(master):
    fn.init_folders()
    row_colors = cycle(row_colors_raw)

    entry_widget_arguments = {'file_path': {'button_text': 'Choose a file', 'initial_dir': result_files_path},
                              'framerate': {'label_text': 'Framerate', 'default_value': 30, 'dtype': 'f++',
                                            'auto': False},
                              'font_size': {'label_text': 'Font Size', 'default_value': '10', 'dtype': 'i++'},
                              'font_color': {'label_text': 'Font Color', 'default_value': '#ffffff'},
                              'bg_color': {'label_text': 'Bg Color', 'default_value': '#000000'},
                              'timeout': {'label_text': 'Timeout', 'default_value': '0', 'dtype': 'f+'}, }
    entry_widget_types = {'file_path': cw.FileDialog,
                          'framerate': cw.Entry,
                          'font_size': cw.Entry,
                          'font_color': cw.ColorChooser,
                          'bg_color': cw.ColorChooser,
                          'timeout': cw.Entry, }

    entry_widgets = {}

    for widget in entry_widget_arguments:
        row_color = next(row_colors)
        entry_widgets[widget] = entry_widget_types[widget](master, row_color=row_color, **entry_widget_arguments[widget])

    row_color = next(row_colors)
    run_button = cw.Button(master, row_color=row_color, button_text='Run',
                           command=partial(pf.check_settings, entry_widgets, pf.from_file_printer))


if __name__ == '__main__':
    program_frame = tk.Tk()
    program_frame.title('  Real time printer')

    def on_closing():
        program_frame.destroy()
        exit(0)

    program_frame.geometry('')
    program_frame.resizable(False, False)
    program_frame.protocol('WM_DELETE_WINDOW', on_closing)
    main(program_frame)
    program_frame.mainloop()