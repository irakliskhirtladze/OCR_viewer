from pathlib import Path

import cv2
from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import QMessageBox

from models.data_store import DataStore, OCRItem
from ui.generated.ui_mainwindow import Ui_MainWindow
from ui.workers.ocr_thread import OCRThread
from ui.workers.progress_runner import ProgressRunner
from utils.file_utils import save_file_dialog, resource_path, get_dir_dialog
from utils.text_formatter import reconstruct_text
from core.ocr_engine import TesseractEngine, EasyOCREngine
import pymupdf


class OCRController(QObject):
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
        self.data_store.ocrResultsChanged.connect(self.on_ocr_results_changed)
        self.ui.export_pdf_btn.clicked.connect(self.pdf_export_btn_clicked)

        # Progress runner for OCR processing
        self._runner = ProgressRunner(self.ui.centralwidget, "OCR", "Recognizing text...")

    # ===============================
    # Slots
    # ===============================
    @Slot()
    def on_ocr_engine_changed(self):
        self.add_langs_to_combo()

    @Slot()
    def on_ocr_results_changed(self):
        current_img_item = self.data_store.get_current_img_item()
        ocr_item_for_current_img = self.data_store.get_ocr_items().get(current_img_item.id)
        if ocr_item_for_current_img is None:
            self.ui.statusbar.showMessage("No image has been processed for OCR", 5000)
            return

        self.on_show_bboxes_toggled(self.ui.bboxes_chbox.isChecked())

    @Slot(bool)
    def on_show_bboxes_toggled(self, checked: bool):
        """If show bboxes is checked, display bounding boxes and conf scores as overlay for the current image."""
        if checked:
            ocr_items = self.data_store.get_ocr_items()
            current_img_item = self.data_store.get_current_img_item()
            current_ocr_item = ocr_items.get(current_img_item.id)
            if current_ocr_item is not None:
                self.ui.edited_img_viewer.bbox_overlay.set_regions(current_ocr_item)

                avg_conf = current_ocr_item.avg_confidence
                self.ui.avg_conf_lbl.clear()
                self.ui.avg_conf_lbl.setText(f"Average conf: {avg_conf:.2f}")
        else:
            self.ui.edited_img_viewer.bbox_overlay.clear_regions()
            self.ui.avg_conf_lbl.clear()

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
    # Run ocr in separate thread
    # ===============================
    @Slot()
    def on_run_ocr_btn_clicked(self):
        chosen_engine = self.ui.ocr_engine_combo.currentText().lower()
        chosen_lang = self.ui.lang_combo.currentText()
        lang = self.ocr_registry[chosen_engine].langs[chosen_lang]
        edited_img_items = self.data_store.get_edited_images()

        thread = OCRThread(edited_img_items, chosen_engine, self.ocr_registry, lang)
        thread.ocr_finished.connect(self._on_ocr_finished)
        thread.error.connect(self._on_ocr_error)

        self._runner.run(
            thread,
            on_progress=thread.progress,
            on_done=self._on_ocr_done
        )

    @Slot(dict)
    def _on_ocr_finished(self, ocr_items: dict[str, OCRItem]):
        if ocr_items:
            self.data_store.set_ocr_items(ocr_items)
            self.ui.statusbar.showMessage("OCR finished.", 5000)

            current_img_item = self.data_store.get_current_img_item()
            if not current_img_item.is_null() and not ocr_items.get(current_img_item.id).is_null():
                self.ui.bboxes_chbox.setEnabled(True)
                self.ui.export_pdf_btn.setEnabled(True)
        else:
            self.ui.statusbar.showMessage("No OCR items added.", 5000)

    @Slot(str)
    def _on_ocr_error(self, error: str):
        self.ui.statusbar.showMessage(f"OCR error: {error}", 5000)

    def _on_ocr_done(self, cancelled: bool):
        """Called when OCR completes, errors, or is cancelled."""
        if cancelled:
            self.ui.statusbar.showMessage("OCR cancelled.", 5000)

    # ===============================
    # PDF Export
    # ===============================
    @Slot()
    def pdf_export_btn_clicked(self):
        edited_img_items = self.data_store.get_edited_images()
        ocr_items = self.data_store.get_ocr_items()

        # file_path = save_file_dialog(self.ui.centralwidget, "Save PDF",
        #                              directory=resource_path("test_exports").as_posix(), filter_str="PDF (*.pdf)")
        dir_path = get_dir_dialog(self.ui.centralwidget, "Select Directory",
                                  directory=resource_path("test_exports").as_posix())

        if dir_path:
            for img_item in edited_img_items.values():
                cv_img = img_item.image
                img_name = Path(img_item.display_name).stem + ".pdf"

                # Encode image to a memory buffer (e.g., JPEG)
                rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                is_success, buffer = cv2.imencode(".jpg", rgb_img)
                img_bytes = buffer.tobytes()

                with pymupdf.open() as doc:
                    page = doc.new_page(width=cv_img.shape[1], height=cv_img.shape[0])
                    page.insert_image(page.rect, stream=img_bytes)

                    # Place invisible text based on bboxes present on each image
                    ocr_item = ocr_items.get(img_item.id)
                    for region in ocr_item.regions:
                        x, y, w, h = region.bbox
                        text = region.text
                        
                        # Calculate fontsize to fit width
                        fontsize = int(h)
                        font = "helv"
                        while pymupdf.get_text_length(text, fontname=font, fontsize=fontsize) > w and fontsize > 4:
                            fontsize -= 1
                        
                        # Baseline is ~80% down from top (typical for most fonts)
                        baseline_y = int(y) + int(fontsize * 0.8)
                        page.insert_text((int(x), baseline_y), text, fontname=font, fontsize=fontsize, render_mode=3)

                    doc.save(Path(dir_path, img_name))
