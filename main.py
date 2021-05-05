import tkinter as tk

from itertools import cycle

from Program_Files import real_time_printer as rtp
from Program_Files import video_to_frames as vtf
from Program_Files import frames_to_ascii_file as ftaf
from Program_Files import print_from_file as pff

from Program_Files import custom_widgets as cw
from Program_Files import styles

if __name__ == '__main__':

    name_dict = {'Real time printer': rtp,
                 'Convert video to frames': vtf,
                 'Convert frames to ascii file': ftaf,
                 'Print from file': pff}

    window = tk.Tk()
    window.title('  Select what to do')

    def on_closing():
        window.destroy()
        exit(0)

    window.geometry('')
    window.resizable(False, False)
    window.protocol('WM_DELETE_WINDOW', on_closing)

    root = tk.Frame(window)
    root.pack()

    def get_run_function(f):
        def run():
            global root
            root.destroy()

            root = tk.Frame(window)
            root.pack()

            program_frame = tk.Frame(root)
            program_frame.pack(side=tk.RIGHT)
            f(program_frame)

            back_button_frame = tk.Frame(root, width=10)
            back_button_frame.pack_propagate(0)
            back_button = tk.Button(back_button_frame, text='', command=draw_interface, bg=styles.back_button_color,
                                    activebackground=styles.back_button_active_color, relief='flat', bd=0)
            back_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
            back_button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

        return run

    def draw_interface():
        global root
        root.destroy()
        root = tk.Frame(window)
        root.pack()
        row_colors = cycle(styles.row_colors_raw)

        for name, package in name_dict.items():
            row_color = next(row_colors)
            cw.Button(root, row_color=row_color, button_text=name, command=get_run_function(package.main))


    draw_interface()

    window.mainloop()
