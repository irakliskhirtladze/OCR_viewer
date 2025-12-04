from PySide6.QtCore import Slot

from ui.generated.ui_mainwindow import Ui_MainWindow


class OCRManager(object):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui

        self.easyocr_langs = {"en": "English", "fr": "French", "de": "German"}
        self.tesseract_langs = {"en": "English", "ge": "Georgian"}

        self.add_langs_to_combo()

        # Signal-slot bindings
        self.ui.ocr_engine_combo.currentTextChanged.connect(self.on_ocr_engine_changed)

    # ===============================
    # Slots
    # ===============================
    @Slot()
    def on_ocr_engine_changed(self):
        self.add_langs_to_combo()

    # ===============================
    # Other logic
    # ===============================
    def add_langs_to_combo(self):
        if self.ui.ocr_engine_combo.currentText() == "Tesseract":
            self.ui.lang_combo.clear()
            self.ui.lang_combo.addItems(self.tesseract_langs.values())
        elif self.ui.ocr_engine_combo.currentText() == "EasyOCR":
            self.ui.lang_combo.clear()
            self.ui.lang_combo.addItems(self.easyocr_langs.values())
