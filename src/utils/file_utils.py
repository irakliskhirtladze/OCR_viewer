import sys
from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QErrorMessage, QWidget


def resource_path(rel: str | Path) -> Path:
    """Return absolute path to a bundled resource (PyInstaller) or project file (dev)."""
    if getattr(sys, "frozen", False):  # running as PyInstaller bundle
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base = Path(__file__).resolve().parent.parent.parent
    return (base / rel).resolve()


def get_app_data_dir() -> Path:
    """Get platform-appropriate app data directory."""
    app_name = "OCRViewer"

    if sys.platform == "win32":
        base = Path.home() / "AppData" / "Local"
    elif sys.platform == "darwin":  # macOS
        base = Path.home() / "Library" / "Application Support"
    else:  # Linux
        base = Path.home() / ".local" / "share"

    app_dir = base / app_name
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_cache_dir() -> Path:
    cache = get_app_data_dir() / "cache"
    cache.mkdir(exist_ok=True)
    return cache


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
        file_paths, _ = QFileDialog.getOpenFileNames(parent, caption, directory, filter_str)
        return file_paths if file_paths else None
    else:
        file_path, _ = QFileDialog.getOpenFileName(parent, caption, directory, filter_str)
        return file_path if file_path else None


def save_file_dialog(parent: QWidget | None = None, caption="Save File", directory="",
                     filter_str="All Files (*)") -> str | None:
    """Allow user to save a file to selected directory."""
    file_path, _ = QFileDialog.getSaveFileName(parent, caption, directory, filter_str)
    return file_path


def get_dir_dialog(parent: QWidget | None = None, caption: str = "Select Directory", directory: str = "") -> str | None:
    dir_path = QFileDialog.getExistingDirectory(
        parent=parent,
        caption=caption,
        dir=directory
    )
    return dir_path if dir_path else None
