from PySide6.QtCore import QThread, Signal

from models.data_store import ImageItem


class ImageProcessorThread(QThread):
    progress = Signal(int, int, str)  # current, total, message
    finished_processing = Signal(dict)  # emits a dict of processed imageitems
    error = Signal(str)

    def __init__(self, img_items: dict[str, ImageItem], filters: list, parent=None):
        super().__init__(parent)
        self.img_items = img_items
        self.filters = filters
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        # Check the number of items to be processed
        total_items = len(self.img_items)
        if total_items == 0:
            self.finished_processing.emit(self.img_items)
            return

        current_item = 0
        edited_img_items = {}

        try:
            for img_id, img_item in self.img_items.items():
                if self._cancelled:
                    break

                self.progress.emit(current_item, total_items, img_id)

                cv_img = img_item.image
                for filt in self.filters:
                    cv_img = filt.apply_filter(cv_img)

                edited_img_item = ImageItem(cv_img, img_item.path, img_item.page)
                edited_img_items[edited_img_item.id] = edited_img_item
                current_item += 1

            # Emit final progress to show 100% before finishing
            self.progress.emit(total_items, total_items, "Done")

            # Small delay to let progress signal be processed first
            self.msleep(10)

            self.finished_processing.emit(edited_img_items)

        except Exception as e:
            self.error.emit(str(e))
