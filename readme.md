# OCR viewer
This app is supposed to work as visual multi-tool software for complex OCR tasks.

The goal is to have an extensible software that can work on batch of images/PDF; apply OpenCV processing
on them visually; Try different OCR engines, such as Tesseract, EasyOCR, TrOCR, etc...; Being able to fine
tune deep learning models; preserve document layouts, export files, and maybe more as needed.

The app is intended to be suitable for OCR specialists and developers able to customize source 
code to add/modify certain features.

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