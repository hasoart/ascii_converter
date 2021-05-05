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

    def entry_control(option):
        if option == 'size':
            entry_widgets['frame_width'].set_state('normal')
            entry_widgets['frame_height'].set_state('normal')
            entry_widgets['scale'].set_state('disabled')
        elif option == 'scale':
            entry_widgets['frame_width'].set_state('disabled')
            entry_widgets['frame_height'].set_state('disabled')
            entry_widgets['scale'].set_state('normal')

    entry_widget_arguments = {'file_path': {'button_text': 'Choose a file', 'initial_dir': source_path},
                              'mode': {'options': ('size', 'scale'), 'options_labels': ('Size', 'Scale'),
                                       'default_value': 'scale', 'command': entry_control},
                              'scale': {'label_text': 'Scale', 'default_value': '1', 'dtype': 'f++'},
                              'frame_height': {'label_text': 'Frame Height', 'default_value': '50', 'dtype': 'i++',
                                               'auto': True, 'state': 'disabled'},
                              'frame_width': {'label_text': 'Frame Width', 'default_value': 'auto', 'dtype': 'i++',
                                              'auto': True, 'state': 'disabled'}}
    entry_widget_types = {'file_path': cw.FileDialog,
                          'mode': cw.RadioButton,
                          'scale': cw.Entry,
                          'frame_height': cw.Entry,
                          'frame_width': cw.Entry}

    entry_widgets = {}

    for widget in entry_widget_arguments:
        row_color = next(row_colors)
        entry_widgets[widget] = entry_widget_types[widget](master, row_color=row_color, **entry_widget_arguments[widget])

    row_color = next(row_colors)
    run_button = cw.Button(master, row_color=row_color, button_text='Run',
                           command=partial(pf.check_settings, entry_widgets,
                                           partial(pf.convert_to_frames, row_color=row_color, master=master)))


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
