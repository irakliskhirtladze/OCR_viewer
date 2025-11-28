import cv2
import numpy as np
import pandas as pd
from PIL import Image
from pytesseract import pytesseract, Output
import easyocr


def orc_tesseract(img: np.ndarray, lang: str = "eng", conf_threshold: int = 10) -> list[dict]:
    """Takes OpenCV image and extracts OCR data from it using tesseract."""
    data = pytesseract.image_to_data(img, lang=lang, config="--psm 3", output_type=Output.DATAFRAME)
    words = data[(data.level == 5) & (data.conf >= conf_threshold)]
    words = words[['text', 'conf', 'left', 'top', 'width', 'height']]
    words = words[words.text.str.strip().astype(bool)]
    words = words.reset_index(drop=True)

    return words.to_dict(orient="records")


def ocr_easyocr(img: np.ndarray, lang: str = "en") -> list:
    """Takes OpenCV image and extracts OCR data from it using easyocr."""
    reader = easyocr.Reader([lang])
    return reader.readtext(img, detail=0, paragraph=True)



