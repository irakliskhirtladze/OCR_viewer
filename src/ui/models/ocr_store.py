from PySide6.QtCore import Signal, QObject, QRect


class OCRStore(QObject):
    result_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._result: list[dict] | None = None

    def get_result(self) -> list[dict] | None:
        """returns current text from store instance"""
        return self._result

    def set_result(self, result: list[dict]) -> None:
        """Sets current text to store instance"""
        self._result = result
        self.result_changed.emit(result)


