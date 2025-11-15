import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract, Output


def orc_tesseract(img: np.ndarray, lang: str = "eng") -> dict:
    """Takes OpenCV image and extracts OCR data from it."""
    data = pytesseract.image_to_data(img, lang=lang, config="--psm 3", output_type=Output.DICT)
    return data


