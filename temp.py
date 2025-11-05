import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from numpy.ma.extras import median

from src.core.ocr_engine import sample_ocr
from src.core.processor import auto_deskew, to_gray, to_binary, invert, dilate, remove_borders
from utils.file_utils import resource_path

if __name__ == '__main__':
    image_file = resource_path("data/page_01.jpg").as_posix()
    rotated_file = resource_path("data/page_01_rotated_no_border.JPG").as_posix()
    rotated_file_bordered = resource_path("data/page_01_rotated.JPG").as_posix()

    # OpenCV images
    img = cv2.imread(rotated_file_bordered)
    copied_img = img.copy()

    # processing
    grey = to_gray(img)
    unbordered = remove_borders(grey)

    deskewed = auto_deskew(img)
    grey = to_gray(deskewed)

    im_bw = to_binary(grey, 210, 255)
    inverted = invert(im_bw)

    kernel = np.ones((1, 1), np.uint8)
    dilated = dilate(inverted, kernel, 1)
    inverted = invert(dilated)

    Image.fromarray(unbordered).show()
