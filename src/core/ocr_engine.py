import time
import cv2
from PIL import Image
from pytesseract import pytesseract

from src.utils.utils import resource_path


def sample_ocr() -> None:
    image_file = resource_path("resources/data/page_01.jpg").as_posix()
    img = cv2.imread(image_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)

    Image.fromarray(im_bw).show()

    text = pytesseract.image_to_string(im_bw)
    print(text)
