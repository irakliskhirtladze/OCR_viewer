from PySide6.QtCore import QThread, Signal

from models.data_store import ImageItem, OCRItem


class OCRThread(QThread):
    progress = Signal(int, int, str)  # current, total, message
    ocr_finished = Signal(dict)  # emits a dict of OCRItems
    error = Signal(str)

    def __init__(self, edited_img_items: dict[str, ImageItem], ocr_engine: str, ocr_registry: dict,
                 lang: str, parent=None):
        super().__init__(parent)
        self.edited_img_items = edited_img_items
        self.ocr_engine = ocr_engine
        self.ocr_registry = ocr_registry
        self.lang = lang
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        total_items = len(self.edited_img_items)
        if total_items == 0:
            self.ocr_finished.emit(self.edited_img_items)
            return

        current_item = 0
        ocr_items = {}
        ocr_engine = self.ocr_registry[self.ocr_engine]()

        try:
            for img_id, edited_img_item in self.edited_img_items.items():
                self.progress.emit(current_item, edited_img_item, img_id)
                regions = ocr_engine.recognize(edited_img_item.image, lang=self.lang)
                ocr_item = OCRItem(img_id, regions, engine=self.ocr_engine, language=self.lang)
                ocr_items[img_id] = ocr_item
                current_item += 1

                # Emit final progress to show 100% before finishing
                self.progress.emit(total_items, total_items, "Done")

                # Small delay to let progress signal be processed first
                self.msleep(10)

                self.ocr_finished.emit(ocr_items)

        except Exception as e:
            self.error.emit(str(e))
