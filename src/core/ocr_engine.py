import cv2
import numpy as np
import pandas as pd
from PIL import Image
from pytesseract import pytesseract, Output
import easyocr
from abc import ABC, abstractmethod

from models.data_store import TextRegion


class OCREngineBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def langs(self) -> dict[str, str]:
        pass

    @abstractmethod
    def recognize(self, image: np.ndarray, lang: str) -> list[TextRegion]:
        """Returns normalized TextRegion list"""
        pass


class TesseractEngine(OCREngineBase):
    name = "tesseract"
    langs = {"English": "eng", "Georgian": "kat"}

    def recognize(self, image: np.ndarray, lang: str) -> list[TextRegion]:
        data = pytesseract.image_to_data(image, lang=lang, output_type=Output.DICT)
        regions = []
        for i in range(len(data['text'])):
            if data['conf'][i] > 0 and data['text'][i].strip():
                regions.append(TextRegion(
                    text=data['text'][i],
                    confidence=data['conf'][i] / 100.0,  # Normalize to 0-1
                    bbox=(data['left'][i], data['top'][i],
                          data['width'][i], data['height'][i]),
                    level="word"
                ))
        return regions


class EasyOCREngine(OCREngineBase):
    name = "easyocr"
    langs = {'English': 'en', 'French': 'fr', 'German': 'de'}

    def recognize(self, image: np.ndarray, lang: str) -> list[TextRegion]:
        reader = easyocr.Reader([lang])
        results = reader.readtext(image)  # Returns [polygon, text, conf]
        regions = []
        for polygon, text, conf in results:
            # Convert 4-point polygon to bbox
            xs = [p[0] for p in polygon]
            ys = [p[1] for p in polygon]
            bbox = (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
            regions.append(TextRegion(
                text=text,
                confidence=conf,
                bbox=bbox,
                level="line"  # EasyOCR returns lines, not words
            ))
        return regions


