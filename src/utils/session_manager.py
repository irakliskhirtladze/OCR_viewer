import json
import os
from pathlib import Path

import numpy as np
from PySide6.QtCore import QSignalBlocker

from models.data_store import DataStore, ImageItem
from ui.generated.ui_mainwindow import Ui_MainWindow
from utils.file_utils import get_app_data_dir, get_cache_dir


class SessionManager:
    """Persists and restores session state to a JSON file."""

    def __init__(self):
        self._session_file = get_app_data_dir() / "session.json"
        self._cache_dir = get_cache_dir()

    def has_saved_session(self) -> bool:
        """Return True if a saved session exists."""
        return self._session_file.exists()

    def _atomic_write(self, state: dict) -> None:
        """Write JSON atomically to avoid corruption."""
        tmp = self._session_file.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        os.replace(tmp, self._session_file)

    def _load(self) -> dict | None:
        """Load JSON"""
        if not self._session_file.exists():
            return None
        try:
            with open(self._session_file, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def save(self, *, data_store: DataStore, ui: Ui_MainWindow | None = None) -> None:
        """Persist image paths and UI state to JSON, cache images as .npy."""
        state = {
            "images": self._collect_images(data_store),
            "current_id": self._get_current_id(data_store),
        }
        if ui:
            state["filters"] = self._collect_filters(ui)
            state["ocr_settings"] = self._collect_ocr_settings(ui)

        self._atomic_write(state)

    def restore(self, *, data_store: DataStore, ui: Ui_MainWindow | None = None) -> bool:
        """Load and apply saved session. Returns True if restored."""
        state = self._load()
        if not state:
            return False

        self._restore_images(data_store, state.get("images", {}), state.get("current_id", ""))

        if ui:
            self._restore_filters(ui, state.get("filters", {}))
            self._restore_ocr_settings(ui, state.get("ocr_settings", {}))

        return True

    def clear(self) -> None:
        """Delete session file and cached images."""
        if self._session_file.exists():
            self._session_file.unlink()
        for f in self._cache_dir.glob("*.npy"):
            f.unlink()

    # ============================================================
    # save restore concrete widget states, files, etc
    # ============================================================
    def _collect_images(self, data_store: DataStore) -> dict:
        """Cache original images as .npy, return metadata."""
        cached = {}
        for img_id, item in data_store.get_img_items().items():
            cache_path = self._cache_dir / f"{img_id}.npy"
            np.save(cache_path, item.image)
            cached[img_id] = {"cache": str(cache_path), "path": item.path, "page": item.page,
                              "display_name": item.display_name}
        return cached

    def _get_current_id(self, data_store: DataStore) -> str:
        current = data_store.get_current_img_item()
        return current.id if not current.is_null() else ""

    def _collect_filters(self, ui: Ui_MainWindow) -> dict:
        return {
            "grey": ui.grey_chbx.isChecked(),
            "binary": ui.binarize_chbx.isChecked(),
            "binary_val": ui.binarize_slider.value(),
            "binary_enabled": ui.binarize_slider.isEnabled(),
            "binary_lbl": ui.binarize_val_lbl.text(),
            "invert": ui.invert_chbx.isChecked(),
            "median": ui.median_chbx.isChecked(),
            "median_k": ui.median_ksize_spinbox.value(),
            "median_k_enabled": ui.median_ksize_spinbox.isEnabled(),
            "dilate_erode": ui.dilate_erode_chbx.isChecked(),
            "dilate": ui.dilate_radio.isChecked(),
            "dilate_enabled": ui.dilate_radio.isEnabled(),
            "erode": ui.erode_radio.isChecked(),
            "erode_enabled": ui.erode_radio.isEnabled(),
            "dilate_erode_k": ui.dilate_erode_ksize_spinbox.value(),
            "dilate_erode_k_enabled": ui.dilate_erode_ksize_spinbox.isEnabled(),
            "dilate_erode_iter": ui.dilate_erode_iter_spinbox.value(),
            "dilate_erode_iter_enabled": ui.dilate_erode_iter_spinbox.isEnabled(),
        }

    def _collect_ocr_settings(self, ui: Ui_MainWindow) -> dict:
        return {
            "engine": ui.ocr_engine_combo.currentText(),
            "language": ui.lang_combo.currentText(),
            "show_bboxes": ui.bboxes_chbox.isChecked(),
        }

    def _restore_images(self, data_store: DataStore, images: dict, current_id: str) -> None:
        items = {}
        for img_id, info in images.items():
            cache_path = Path(info["cache"])
            if cache_path.exists():
                items[img_id] = ImageItem(
                    image=np.load(cache_path),
                    path=info["path"],
                    page=info.get("page"),
                    display_name=info["display_name"],
                    id=img_id,
                )
        if items:
            data_store.add_img_items(items)
            if current_id and current_id in items:
                data_store.set_current_img_item(items[current_id])

    def _restore_filters(self, ui: Ui_MainWindow, f: dict) -> None:
        widgets = [
            ui.grey_chbx, ui.binarize_chbx, ui.binarize_slider,
            ui.invert_chbx, ui.median_chbx, ui.median_ksize_spinbox,
            ui.dilate_erode_chbx, ui.dilate_radio, ui.erode_radio,
            ui.dilate_erode_ksize_spinbox, ui.dilate_erode_iter_spinbox,
        ]
        blockers = [QSignalBlocker(w) for w in widgets]
        try:
            ui.grey_chbx.setChecked(f.get("grey", False))
            ui.binarize_chbx.setChecked(f.get("binary", False))
            ui.binarize_slider.setValue(f.get("binary_val", 127))
            ui.binarize_slider.setEnabled(f.get("binary_enabled", False))
            ui.binarize_val_lbl.setText(f.get("binary_lbl", ""))
            ui.invert_chbx.setChecked(f.get("invert", False))
            ui.median_chbx.setChecked(f.get("median", False))
            ui.median_ksize_spinbox.setValue(f.get("median_k", 3))
            ui.median_ksize_spinbox.setEnabled(f.get("median_k_enabled", False))
            ui.dilate_erode_chbx.setChecked(f.get("dilate_erode", False))
            ui.dilate_radio.setChecked(f.get("dilate", True))
            ui.dilate_radio.setEnabled(f.get("dilate_enabled", False))
            ui.erode_radio.setChecked(f.get("erode", False))
            ui.erode_radio.setEnabled(f.get("erode_enabled", False))
            ui.dilate_erode_ksize_spinbox.setValue(f.get("dilate_erode_k", 2))
            ui.dilate_erode_ksize_spinbox.setEnabled(f.get("dilate_erode_k_enabled", False))
            ui.dilate_erode_iter_spinbox.setValue(f.get("dilate_erode_iter", 1))
            ui.dilate_erode_iter_spinbox.setEnabled(f.get("dilate_erode_iter_enabled", False))
        finally:
            del blockers

    def _restore_ocr_settings(self, ui: Ui_MainWindow, s: dict) -> None:
        blockers = [
            QSignalBlocker(ui.ocr_engine_combo),
            QSignalBlocker(ui.lang_combo),
            QSignalBlocker(ui.bboxes_chbox),
        ]
        try:
            if s.get("engine"):
                ui.ocr_engine_combo.setCurrentText(s["engine"])
            if s.get("language"):
                ui.lang_combo.setCurrentText(s["language"])
            ui.bboxes_chbox.setChecked(s.get("show_bboxes", False))
        finally:
            del blockers
