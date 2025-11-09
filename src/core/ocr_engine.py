import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract


def orc_tesseract(img: np.ndarray, lang: str = "eng") -> str:
    """Takes OpenCV image and extracts OCR text from it."""
    text = pytesseract.image_to_string(img, lang=lang, config="--psm 3")
    return text
