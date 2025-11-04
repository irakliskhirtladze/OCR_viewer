import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.core.ocr_engine import sample_ocr


if __name__ == '__main__':
    sample_ocr()
