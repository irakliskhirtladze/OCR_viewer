import numpy as np
from PySide6.QtGui import QImage


def qimage_to_cv(qimg: QImage) -> np.ndarray:
    if qimg is None or qimg.isNull():
        return None
    qimg = qimg.convertToFormat(QImage.Format.Format_RGBA8888)
    w, h = qimg.width(), qimg.height()
    ptr = qimg.bits()
    
    # Handle both old sip.voidptr and new memoryview
    if hasattr(ptr, 'setsize'):
        ptr.setsize(qimg.sizeInBytes())
        arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 4))
    else:
        # memoryview (newer PySide6)
        arr = np.array(ptr).reshape((h, w, 4))
    
    # RGBA -> BGR
    bgr = arr[..., :3][:, :, ::-1].copy()
    return bgr


def cv_to_qimage(img: np.ndarray) -> QImage:
    if img.ndim == 2:
        h, w = img.shape
        rgba = np.stack([img, img, img, np.full((h, w), 255, np.uint8)], axis=2)
    else:
        # BGR -> RGBA
        rgba = np.concatenate([img[:, :, ::-1], 255*np.ones((*img.shape[:2], 1), np.uint8)], axis=2)
    h, w = rgba.shape[:2]
    q = QImage(rgba.data, w, h, w*4, QImage.Format.Format_RGBA8888)
    return q.copy()
