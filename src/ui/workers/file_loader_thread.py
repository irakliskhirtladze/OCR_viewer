from pathlib import Path

import cv2
import numpy as np
import pymupdf
from PySide6.QtCore import QThread, Signal

from models.data_store import ImageItem


class FileLoaderThread(QThread):
    """Worker thread for loading image files with progress reporting."""

    progress = Signal(int, int, str)  # (current, total, filename)
    finished_loading = Signal(dict)  # {id: ImageItem}
    error = Signal(str)

    def __init__(self, file_paths: list[str], parent=None):
        super().__init__(parent)
        self.file_paths = file_paths
        self._cancelled = False

    def cancel(self):
        """Request cancellation of the loading process."""
        self._cancelled = True

    def run(self):
        """Load files in background thread."""
        image_dict = {}

        # First pass: count total items (files + PDF pages)
        total_items = 0
        for file_path in self.file_paths:
            if self._cancelled:
                break
            if file_path.lower().endswith(".pdf"):
                try:
                    with pymupdf.open(file_path) as doc:
                        total_items += len(doc)
                except Exception:
                    total_items += 1  # Count as 1 if can't open
            else:
                total_items += 1

        if total_items == 0:
            self.finished_loading.emit(image_dict)
            return

        # Second pass: load with per-item progress
        current_item = 0

        try:
            for file_path in self.file_paths:
                if self._cancelled:
                    break

                if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.progress.emit(current_item, total_items, Path(file_path).name)
                    cv_img = cv2.imread(file_path)
                    if cv_img is not None:
                        img_item = ImageItem(cv_img, file_path)
                        image_dict[img_item.id] = img_item
                    current_item += 1

                elif file_path.lower().endswith(".pdf"):
                    with pymupdf.open(file_path) as doc:
                        pdf_name = Path(file_path).name
                        for page_num in range(len(doc)):
                            if self._cancelled:
                                break

                            # Emit progress for each page
                            self.progress.emit(
                                current_item,
                                total_items,
                                f"{pdf_name} (page {page_num + 1}/{len(doc)})"
                            )

                            page = doc.load_page(page_num)
                            pix = page.get_pixmap(alpha=False)
                            cv_img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                                pix.height, pix.width, 3
                            )
                            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
                            img_item = ImageItem(cv_img, file_path, page=page_num)
                            image_dict[img_item.id] = img_item
                            current_item += 1

            self.finished_loading.emit(image_dict)

        except Exception as e:
            self.error.emit(str(e))
