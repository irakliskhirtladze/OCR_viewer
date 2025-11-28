# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

from ui.widgets.base_widgets.h_scroll_area import HorizontalThumbnailScrollArea
from ui.widgets.edited_img_viewer import EditedImageViewer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1078, 613)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_cont = QFrame(self.centralwidget)
        self.left_cont.setObjectName(u"left_cont")
        self.left_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.left_cont)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.file_load_cont = QFrame(self.left_cont)
        self.file_load_cont.setObjectName(u"file_load_cont")
        self.file_load_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.file_load_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.file_load_cont)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.button_bar_cont = QFrame(self.file_load_cont)
        self.button_bar_cont.setObjectName(u"button_bar_cont")
        self.button_bar_cont.setMaximumSize(QSize(16777215, 50))
        self.button_bar_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.button_bar_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.button_bar_cont)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.choose_files_btn = QPushButton(self.button_bar_cont)
        self.choose_files_btn.setObjectName(u"choose_files_btn")
        self.choose_files_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.choose_files_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.clear_all_btn = QPushButton(self.button_bar_cont)
        self.clear_all_btn.setObjectName(u"clear_all_btn")
        self.clear_all_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.clear_all_btn)


        self.verticalLayout_2.addWidget(self.button_bar_cont)

        self.thumb_scroll_area = HorizontalThumbnailScrollArea(self.file_load_cont)
        self.thumb_scroll_area.setObjectName(u"thumb_scroll_area")
        self.thumb_scroll_area.setMinimumSize(QSize(0, 100))
        self.thumb_scroll_area.setMaximumSize(QSize(16777215, 100))
        self.thumb_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.thumb_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.thumb_scroll_area.setWidgetResizable(True)
        self.thumb_scroll_widget = QWidget()
        self.thumb_scroll_widget.setObjectName(u"thumb_scroll_widget")
        self.thumb_scroll_widget.setGeometry(QRect(0, 0, 485, 86))
        self.thumb_scroll_area.setWidget(self.thumb_scroll_widget)

        self.verticalLayout_2.addWidget(self.thumb_scroll_area)


        self.verticalLayout.addWidget(self.file_load_cont)

        self.edited_img_viewer = EditedImageViewer(self.left_cont)
        self.edited_img_viewer.setObjectName(u"edited_img_viewer")
        self.edited_img_viewer.setFrameShape(QFrame.Shape.StyledPanel)
        self.edited_img_viewer.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.edited_img_viewer)

        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.left_cont)

        self.right_cont = QFrame(self.centralwidget)
        self.right_cont.setObjectName(u"right_cont")
        self.right_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.right_cont)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.text_edit = QTextEdit(self.right_cont)
        self.text_edit.setObjectName(u"text_edit")

        self.horizontalLayout_2.addWidget(self.text_edit)

        self.filter_cont = QFrame(self.right_cont)
        self.filter_cont.setObjectName(u"filter_cont")
        self.filter_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.filter_cont.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_2.addWidget(self.filter_cont)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.right_cont)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.choose_files_btn.setText(QCoreApplication.translate("MainWindow", u"Choose files", None))
        self.clear_all_btn.setText(QCoreApplication.translate("MainWindow", u"Clear all", None))
    # retranslateUi

