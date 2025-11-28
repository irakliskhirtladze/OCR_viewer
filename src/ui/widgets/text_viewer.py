from PySide6.QtWidgets import QVBoxLayout, QFrame, QTextEdit, QSizePolicy

from ui.models.ocr_store import OCRStore
from utils.words_to_text import reconstruct_text


class TextViewerWidget(QFrame):
    def __init__(self, ocr_store: OCRStore):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("border: 1px solid grey;")
        self.layout().addWidget(self.text_edit)

        self.ocr_store = ocr_store
        self.ocr_store.result_changed.connect(self._on_result_changed)

    def _on_result_changed(self, result: list | None) -> None:
        text = reconstruct_text(result)
        self.text_edit.setText(text)
