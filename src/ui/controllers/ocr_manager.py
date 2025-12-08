from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox, QProgressDialog

from models.data_store import DataStore, OCRItem
from ui.generated.ui_mainwindow import Ui_MainWindow
from ui.workers.ocr_worker import OCRThread
from utils.image_converter import cv_to_qimage, qimage_to_cv
from utils.text_formatter import reconstruct_text
from core.ocr_engine import TesseractEngine, EasyOCREngine


class OCRManager(object):
    def __init__(self, ui: Ui_MainWindow, data_store: DataStore):
        super().__init__()
        self.ui = ui
        self.data_store = data_store

        # setup ocr engine and supported language boxes
        self.easyocr_langs = {'English': 'en', 'French': 'fr', 'German': 'de'}
        self.tesseract_langs = {"English": "eng", "Georgian": "kat"}
        self.add_langs_to_combo()

        # OCR engine registry
        self.ocr_registry = {
            TesseractEngine.name: TesseractEngine,
            EasyOCREngine.name: EasyOCREngine,
        }

        # Signal-slot bindings
        self.ui.ocr_engine_combo.currentTextChanged.connect(self.on_ocr_engine_changed)
        self.ui.run_ocr_btn.clicked.connect(self.on_run_ocr_btn_clicked)
        self.ui.show_bboxes_btn.clicked.connect(self.on_show_bboxes_clicked)
        self.data_store.ocrResultsChanged.connect(self.on_ocr_results_changed)

        # Init progress bar and worker with none
        self._progress_dialog: QProgressDialog | None = None
        self._ocr_thread: OCRThread | None = None

    # ===============================
    # Slots
    # ===============================
    @Slot()
    def on_ocr_engine_changed(self):
        self.add_langs_to_combo()

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

        text = "Sample text"
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

    # ===============================
    # Run tesseract ocr in separate thread
    # ===============================
    @Slot()
    def on_run_ocr_btn_clicked(self):
        chosen_engine = self.ui.ocr_engine_combo.currentText()
        chosen_lang = self.ui.lang_combo.currentText()
        edited_img_items = self.data_store.get_ocr_items()

        # progress dialog
        self._progress_dialog = QProgressDialog("Recognizing text...", "Cancel", 0, 0, self.ui.centralwidget)
