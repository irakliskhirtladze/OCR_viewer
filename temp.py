import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from numpy.ma.extras import median

from src.backend.processor import auto_deskew, to_gray, to_binary, invert, dilate, remove_borders, gaussian_blur
from utils.file_utils import resource_path

if __name__ == '__main__':
    image_file = resource_path("data/page_01.jpg").as_posix()
    rotated_file = resource_path("data/page_01_rotated_no_border.JPG").as_posix()
    rotated_file_bordered = resource_path("data/page_01_rotated.JPG").as_posix()
    ninety = resource_path("data/90.png").as_posix()

    # OpenCV images
    img = cv2.imread(image_file)

    # # processing
    # grey = to_gray(img)
    # unbordered = remove_borders(grey)
    #
    # gaussian = gaussian_blur(unbordered, (19, 1))
    #
    # deskewed = auto_deskew(img)
    # grey = to_gray(deskewed)
    #
    # im_bw = to_binary(grey, 210, 255)
    # inverted = invert(im_bw)

    dilated = dilate(img, (3, 3), 1)

    Image.fromarray(dilated).show()
