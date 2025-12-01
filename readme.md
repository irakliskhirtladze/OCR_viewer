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