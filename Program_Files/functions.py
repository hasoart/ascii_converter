from numba import njit
import os
from Program_Files.paths import *


@njit(cache=True)
def join_1d(arr):
    txt = ''.join(arr) + '\n'
    return txt


@njit(cache=True)
def join_2d_array_to_frame(char_img):
    txt = ''.join([join_1d(row) for row in char_img])
    return txt


@njit(cache=True)
def join_2d_array(char_img):
    txt = join_2d_array_to_frame(char_img) + '|\n'
    return txt


def init_folders():
    list_dir = os.listdir(main_dir)
    if 'Source' not in list_dir:
        os.makedirs(source_path)
    if 'Result_Files' not in list_dir:
        os.makedirs(result_files_path)
    if 'Extracted_Frames' not in list_dir:
        os.makedirs(extracted_frames_path)
