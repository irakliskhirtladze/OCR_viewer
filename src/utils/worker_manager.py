import sys
import traceback

from PySide6.QtCore import QObject, Signal, Slot, QRunnable, Qt
from PySide6.QtWidgets import QApplication


class WorkerSignals(QObject):
    completed = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            QApplication.restoreOverrideCursor()
            self.signals.completed.emit()
