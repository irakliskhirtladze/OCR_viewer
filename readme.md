# OCR viewer
This app is supposed to work as visual opencv batch editor and  multi-engine OCR software.

Currently, it has support for 2 OCR engines with few languages for testing.

### Current features:
* Batch import images and pdf's as OpenCV images
* Apply OpenCV preprocessing for better OCR accuracy
* Run tesseract or easyocr with few languages on loaded images to extract text
* Apply bounding boxes (bboxes) to preview results, evaluate accuracy and edit results manually if desired
* Export results as searchable PDFs

### Planned features
* adding deskew algorithm for automatic image transformation
* add yolo + huggingface transformer (likely TrOCR) as advanced ocr solution.
One of the goals is to make it Georgian language compatible
* other UX improvements

# PySide instructions
To generate .py from .ui file:
```
pyside6-uic src/ui/generated/mainwindow.ui -o src/ui/generated/ui_mainwindow.py
```

# Packaging instructions
* Install pyinstallr in your .venv:
```
pip install pyinstaller
```
* Generate .spec file
```
pyi-makespec --windowed --name "OCR Viewer" src/main.py
```
* Edit .spec file as needed. Likely only these parts need change:

pathex=["src"]

datas=[ ('src/ui/resources/styles.qss', 'ui/resources'), ]

* Build using:
```
pyinstaller "OCR Viewer.spec"
```