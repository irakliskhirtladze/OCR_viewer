import cv2
import numpy as np
from PIL import Image


def remove_borders(image: np.ndarray):
    """Automatically remove borders from Greyscale image if they exist"""
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt_sorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cnt_sorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    return image[y:y + h, x:x + w]


def get_skew_angle(cv_image: np.ndarray) -> float:
    """Takes BGR image and automatically detects skew angle"""
    # Prep image, copy, convert to gray scale, blur, and threshold
    new_image = cv_image.copy()
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        cv2.rectangle(new_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Find largest contour and surround in min area box
    largest_contour = contours[0]
    min_area_rect = cv2.minAreaRect(largest_contour)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = min_area_rect[-1]
    if angle < -45:
        angle = 90 + angle

    return -1.0 * angle


def rotate_image(cv_image: np.ndarray, angle: float):
    """Rotate the image around its center"""
    new_image = cv_image.copy()
    (h, w) = new_image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    new_image = cv2.warpAffine(new_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return new_image


def auto_deskew(image: np.ndarray):
    angle = get_skew_angle(image)
    return rotate_image(image, -1.0 * angle)


def crop(image: np.ndarray, x1: int, y1: int, x2: int, y2: int):
    """Crops the image to given size"""
    return image[y1:y2, x1:x2]


def to_gray(image: np.ndarray) -> np.ndarray:
    """Converts the image to grayscale"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def invert(image: np.ndarray):
    """Inverts the image colors"""
    return cv2.bitwise_not(image)


def to_binary(image: np.ndarray, threshold: int, max_value: int) -> np.ndarray:
    """Converts the image to binary"""
    return cv2.threshold(image, threshold, max_value, cv2.THRESH_BINARY)[1]


def gaussian_blur(image: np.ndarray, kernel_size: tuple[int, int]) -> np.ndarray:
    """Applies Gaussian blur to the image"""
    return cv2.GaussianBlur(image, kernel_size, 0)


def median_blur(image: np.ndarray, kernel_size: int) -> np.ndarray:
    """Applies median blur to the image"""
    return cv2.medianBlur(image, kernel_size)


def bilateral_filter(image: np.ndarray, d: int, sigma_color: int, sigma_space: int) -> np.ndarray:
    """Applies bilateral filter to the image"""
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


def dilate(image: np.ndarray, kernel: np.ndarray, iterations) -> np.ndarray:
    """Dilate an image"""
    return cv2.dilate(image, kernel, iterations=iterations)


def erode(image: np.ndarray, kernel: np.ndarray, iterations) -> np.ndarray:
    """Erode an image"""
    return cv2.erode(image, kernel, iterations=iterations)
