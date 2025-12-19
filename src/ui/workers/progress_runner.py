from PySide6.QtCore import QThread, Signal, Slot, Qt
from PySide6.QtWidgets import QProgressDialog, QWidget


class ProgressRunner:
    """
    Safe wrapper for running a QThread with a QProgressDialog.
    Handles all race conditions internally.
    """

    def __init__(self, parent: QWidget, title: str = "Processing", label: str = "Working..."):
        self._parent = parent
        self._title = title
        self._label = label
        self._thread: QThread | None = None
        self._dialog: QProgressDialog | None = None
        self._cancelled = False

    def run(self, thread: QThread,
            on_progress: Signal = None,
            on_done: callable = None):
        """
        Start the thread with progress dialog.

        Args:
            thread: QThread with a progress signal
            on_progress: Signal(int, int, str) - current, total, message
            on_done: Callback when everything is complete (success, error, or cancel)
        """
        self._cancelled = False
        self._on_done = on_done
        self._thread = thread

        # Create dialog
        self._dialog = QProgressDialog(self._label, "Cancel", 0, 0, self._parent)
        self._dialog.setWindowTitle(self._title)
        self._dialog.setWindowModality(Qt.WindowModal)
        self._dialog.setMinimumDuration(0)
        self._dialog.canceled.connect(self._handle_cancel)

        # Connect progress signal
        if on_progress:
            on_progress.connect(self._handle_progress)

        # Always use thread.finished for cleanup
        self._thread.finished.connect(self._cleanup)
        self._thread.start()

    @Slot(int, int, str)
    def _handle_progress(self, current: int, total: int, message: str):
        dialog = self._dialog  # Local reference - safe from nested events
        if dialog is not None and not self._cancelled:
            dialog.setMaximum(total)
            dialog.setValue(current)
            dialog.setLabelText(message)

    @Slot()
    def _handle_cancel(self):
        self._cancelled = True
        if self._thread and hasattr(self._thread, 'cancel'):
            self._thread.cancel()

    @Slot()
    def _cleanup(self):
        """Called when thread fully completes - always safe."""
        if self._dialog:
            try:
                self._dialog.canceled.disconnect(self._handle_cancel)
            except RuntimeError:
                pass  # Already disconnected
            self._dialog.close()
            self._dialog = None
        self._thread = None

        if self._on_done:
            self._on_done(cancelled=self._cancelled)

    @property
    def was_cancelled(self) -> bool:
        return self._cancelled
