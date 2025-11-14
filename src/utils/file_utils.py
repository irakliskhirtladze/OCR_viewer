import sys
from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QErrorMessage


def resource_path(rel: str | Path) -> Path:
    """Return absolute path to a bundled resource (PyInstaller) or project file (dev)."""
    if getattr(sys, "frozen", False):  # running as PyInstaller bundle
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base = Path(__file__).resolve().parent.parent.parent
    return (base / rel).resolve()


def open_file_dialog(parent=None, caption="Open File", directory="", filter_str="All Files (*)",
                     multi=False) -> str | list[str] | None:
    """
    Args:
        parent: Parent widget (e.g., self for modal).
        caption: Dialog title.
        directory: Starting dir (e.g., str(Path.home())).
        filter_str: File filter (e.g., "Images (*.png *.jpg)").
        multi: If True, returns list of paths.

    Returns:
        Path str (single), list[str] (multi), or None (cancelled).
    """
    if multi:
        files, _ = QFileDialog.getOpenFileNames(parent, caption, directory, filter_str)
        return files if files else None
    else:
        file_path, _ = QFileDialog.getOpenFileName(parent, caption, directory, filter_str)

        return file_path if file_path else None
