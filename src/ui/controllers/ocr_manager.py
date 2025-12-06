from PySide6.QtCore import Slot

from core.ocr_engine import tesseract_word_data
from models.data_store import DataStore, OCRItem
from ui.generated.ui_mainwindow import Ui_MainWindow
from utils.image_converter import cv_to_qimage, qimage_to_cv
from utils.text_formatter import reconstruct_text


class OCRManager(object):
    def __init__(self, ui: Ui_MainWindow, data_store: DataStore):
        super().__init__()
        self.ui = ui
        self.data_store = data_store

        # setup ocr engine and supported language boxes
        self.easyocr_langs = {'English': 'en', 'French': 'fr', 'German': 'de'}
        self.tesseract_langs = {"English": "eng", "Georgian": "kat"}
        self.add_langs_to_combo()

        # Signal-slot bindings
        self.ui.ocr_engine_combo.currentTextChanged.connect(self.on_ocr_engine_changed)
        self.ui.run_ocr_btn.clicked.connect(self.on_run_ocr_btn_clicked)
        self.ui.show_bboxes_btn.clicked.connect(self.on_show_bboxes_clicked)
        self.data_store.ocrResultsChanged.connect(self.on_ocr_results_changed)

    # ===============================
    # Slots
    # ===============================
    @Slot()
    def on_ocr_engine_changed(self):
        self.add_langs_to_combo()

    @Slot()
    def on_run_ocr_btn_clicked(self):
        ocr_engine = self.ui.ocr_engine_combo.currentText()
        if ocr_engine.lower() == "tesseract":
            self.run_tesseract()
        elif ocr_engine.lower() == "easyocr":
            self.run_easyocr()

    @Slot()
    def on_show_bboxes_clicked(self):
        pass

    @Slot()
    def on_ocr_results_changed(self):
        current_img_item = self.data_store.get_current_img_item()
        ocr_item_for_current_img = self.data_store.get_ocr_items().get(current_img_item.id)
        if ocr_item_for_current_img is None:
            self.ui.statusbar.showMessage("No image has been processed for OCR", 5000)
            return

        print(f"=======  {ocr_item_for_current_img.image_id}")
        text = reconstruct_text(ocr_item_for_current_img.word_data)
        self.ui.text_edit.clear()
        self.ui.text_edit.setText(text)

    # ===============================
    # Other logic
    # ===============================
    def add_langs_to_combo(self):
        if self.ui.ocr_engine_combo.currentText() == "Tesseract":
            self.ui.lang_combo.clear()
            self.ui.lang_combo.addItems(self.tesseract_langs.keys())
        elif self.ui.ocr_engine_combo.currentText() == "EasyOCR":
            self.ui.lang_combo.clear()
            self.ui.lang_combo.addItems(self.easyocr_langs.keys())

    def run_tesseract(self):
        """Run ocr using tesseract on edited images from the store"""
        edited_img_items = self.data_store.get_edited_images()
        ocr_items = {}
        for img_item in edited_img_items.values():
            selected_lang = self.ui.lang_combo.currentText()
            word_data = tesseract_word_data(img_item.image, lang=self.tesseract_langs[selected_lang])
            ocr_item = OCRItem(img_item.id, word_data)
            ocr_items[img_item.id] = ocr_item

        self.data_store.set_ocr_items(ocr_items)

    def run_easyocr(self):
        pass

