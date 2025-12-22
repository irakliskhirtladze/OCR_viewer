from dataclasses import dataclass, field, asdict
from pathlib import Path
import json


@dataclass
class ProjectData:
    """Serializable project state - only what's needed to reconstruct"""
    # Files to reload
    source_images: dict = field(default_factory=dict)

    # Current selection
    current_image_id: str = ""

    # edited images
    edited_images: dict = field(default_factory=dict)

    # Filter settings (to reapply)
    filters: dict = field(default_factory=lambda: {
        "grey": False,
        "binary": {"enabled": False, "threshold": 127},
        "invert": False,
        "median_blur": {"enabled": False, "k_size": 3},
        "dilate_erode": {"enabled": False, "mode": "dilate", "k_size": 2, "iterations": 1}
    })

    # OCR settings
    ocr_engine: str = "tesseract"
    ocr_language: str = "eng"
    show_bboxes: bool = False

    # Meta
    saved_on_close: bool = False

    def save(self, path: Path):
        """Save project to JSON file"""
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "ProjectData":
        """Load project from JSON file"""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

