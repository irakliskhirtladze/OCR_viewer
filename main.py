import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.app import OCRViewer


if __name__ == '__main__':
    app = OCRViewer()
    sys.exit(app.exec())
