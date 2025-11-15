from PySide6.QtWidgets import QVBoxLayout, QFrame, QTextEdit

from ui.models.ocr_store import OCRStore


class TextViewerWidget(QFrame):
    def __init__(self, text_store: OCRStore):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("border: 1px solid grey;")
        self.layout().addWidget(self.text_edit)

        self.text_store = text_store
        self.text_store.text_changed.connect(self._on_text_changed)

    def _on_text_changed(self, text):
        self.text_edit.setText(text)
