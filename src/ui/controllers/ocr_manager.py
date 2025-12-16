from PySide6.QtCore import Slot, Qt, QObject
from PySide6.QtWidgets import QMessageBox, QProgressDialog

from models.data_store import DataStore, OCRItem
from ui.generated.ui_mainwindow import Ui_MainWindow
from ui.workers.ocr_worker import OCRThread
from utils.image_converter import cv_to_qimage, qimage_to_cv
from utils.text_formatter import reconstruct_text
from core.ocr_engine import TesseractEngine, EasyOCREngine


class OCRManager(QObject):
    def __init__(self, ui: Ui_MainWindow, data_store: DataStore):
        super().__init__()
        self.ui = ui
        self.data_store = data_store

        # OCR engine registry
        self.ocr_registry = {
            TesseractEngine.name: TesseractEngine,
            EasyOCREngine.name: EasyOCREngine,
        }

        # setup ocr engine and supported language boxes
        self.add_langs_to_combo()

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
            self.ui.lang_combo.addItems(self.ocr_registry["tesseract"].langs.keys())
        elif self.ui.ocr_engine_combo.currentText() == "EasyOCR":
            self.ui.lang_combo.clear()
            self.ui.lang_combo.addItems(self.ocr_registry["easyocr"].langs.keys())

    # ===============================
    # Run tesseract ocr in separate thread
    # ===============================
    @Slot()
    def on_run_ocr_btn_clicked(self):
        chosen_engine = self.ui.ocr_engine_combo.currentText().lower()

        chosen_lang = self.ui.lang_combo.currentText()
        lang = self.ocr_registry[chosen_engine].langs[chosen_lang]

        edited_img_items = self.data_store.get_img_items()

        # Progress dialog
        self._progress_dialog = QProgressDialog("Recognizing text...", "Cancel", 0, 0, self.ui.centralwidget)
        self._progress_dialog.setWindowTitle("OCR")
        self._progress_dialog.setWindowModality(Qt.WindowModal)
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.canceled.connect(self._on_ocr_cancelled)

        # Worker thread for the OCR batch processing
        self._ocr_thread = OCRThread(edited_img_items, chosen_engine, self.ocr_registry, lang, self)
        self._ocr_thread.progress.connect(self._on_ocr_progress)
        self._ocr_thread.ocr_finished.connect(self._on_ocr_finished)
        self._ocr_thread.error.connect(self._on_ocr_error)
        self._ocr_thread.start()

    @Slot()
    def _on_ocr_cancelled(self):
        if self._ocr_thread:
            self._ocr_thread.cancel()
            self._ocr_thread.wait()
        self._cleanup_thread()
        self.ui.statusbar.showMessage("OCR cancelled.", 5000)

    @Slot(int, int, str)
    def _on_ocr_progress(self, current: int, total: int, filename: str):
        if self._progress_dialog is not None:
            self._progress_dialog.setMaximum(total)
            self._progress_dialog.setValue(current)
            self._progress_dialog.setLabelText(f"Extracting text from {filename}")

    @Slot(dict)
    def _on_ocr_finished(self, ocr_items: dict[str, OCRItem]):
        if ocr_items:
            self.data_store.set_ocr_items(ocr_items)
            self.ui.statusbar.showMessage("OCR finished.", 5000)
        else:
            self.ui.statusbar.showMessage("No OCR items added.", 5000)

    @Slot()
    def _on_thread_finished(self):
        self._cleanup_thread()

    @Slot(str)
    def _on_ocr_error(self, error: str):
        self.ui.statusbar.showMessage(f"OCR error: {error}", 5000)

    def _cleanup_thread(self):
        if self._progress_dialog:
            self._progress_dialog.close()
            self._progress_dialog = None
        self._ocr_thread = None
