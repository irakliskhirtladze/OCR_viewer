import sys
import qdarktheme

from PySide6.QtWidgets import QApplication

from ui.controllers.main_window import MainWindow
from utils.file_utils import resource_path

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # ========= Styling the app =========
    theme_qss = qdarktheme.load_stylesheet(
        theme="dark",
        corner_shape="rounded",
        custom_colors={"primary": "#88E788"}
    )

    # Read the QSS file
    styles_file = resource_path("src/ui/resources/styles.qss").as_posix()
    with open(styles_file, "r") as f:
        custom_qss = f.read()

    # Append custom style to the theme styles
    app.setStyleSheet(theme_qss + "\n" + custom_qss)

    window = MainWindow()
    window.showMaximized()
    app.exec()
