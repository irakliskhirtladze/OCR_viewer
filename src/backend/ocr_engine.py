import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract, Output
import easyocr


def orc_tesseract(img: np.ndarray, lang: str = "eng") -> dict:
    """Takes OpenCV image and extracts OCR data from it using tesseract."""
    data = pytesseract.image_to_data(img, lang=lang, config="--psm 3", output_type=Output.DICT)
    return data


def ocr_easyocr(img: np.ndarray, lang: str = "en") -> list:
    """Takes OpenCV image and extracts OCR data from it using easyocr."""
    reader = easyocr.Reader([lang])
    return reader.readtext(img, detail=0, paragraph=True)



