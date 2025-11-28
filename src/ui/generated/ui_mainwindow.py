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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

from ui.widgets.base_widgets.h_scroll_area import HorizontalThumbnailScrollArea
from ui.widgets.edited_img_viewer import EditedImageViewer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1009, 848)
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
        self.thumb_scroll_widget.setGeometry(QRect(0, 0, 451, 86))
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
        self.control_cont = QFrame(self.right_cont)
        self.control_cont.setObjectName(u"control_cont")
        self.control_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.control_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.control_cont)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.filter_cont = QFrame(self.control_cont)
        self.filter_cont.setObjectName(u"filter_cont")
        self.filter_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.filter_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.filter_cont)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.grey_filter = QFrame(self.filter_cont)
        self.grey_filter.setObjectName(u"grey_filter")
        self.grey_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.grey_filter.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.grey_filter)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.grey_chbx = QCheckBox(self.grey_filter)
        self.grey_chbx.setObjectName(u"grey_chbx")

        self.horizontalLayout_4.addWidget(self.grey_chbx)


        self.verticalLayout_4.addWidget(self.grey_filter)

        self.binary_filter = QFrame(self.filter_cont)
        self.binary_filter.setObjectName(u"binary_filter")
        self.binary_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.binary_filter.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.binary_filter)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.binarize_chbx = QCheckBox(self.binary_filter)
        self.binarize_chbx.setObjectName(u"binarize_chbx")

        self.verticalLayout_5.addWidget(self.binarize_chbx)

        self.frame = QFrame(self.binary_filter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.binarize_slider = QSlider(self.frame)
        self.binarize_slider.setObjectName(u"binarize_slider")
        self.binarize_slider.setMaximum(255)
        self.binarize_slider.setOrientation(Qt.Orientation.Horizontal)
        self.binarize_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.binarize_slider.setTickInterval(0)

        self.horizontalLayout_5.addWidget(self.binarize_slider)

        self.binarize_val_lbl = QLabel(self.frame)
        self.binarize_val_lbl.setObjectName(u"binarize_val_lbl")
        self.binarize_val_lbl.setMinimumSize(QSize(20, 0))
        self.binarize_val_lbl.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_5.addWidget(self.binarize_val_lbl)


        self.verticalLayout_5.addWidget(self.frame)


        self.verticalLayout_4.addWidget(self.binary_filter)

        self.invert_filter = QFrame(self.filter_cont)
        self.invert_filter.setObjectName(u"invert_filter")
        self.invert_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.invert_filter.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_4.addWidget(self.invert_filter)

        self.gaussian_filter = QFrame(self.filter_cont)
        self.gaussian_filter.setObjectName(u"gaussian_filter")
        self.gaussian_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.gaussian_filter.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_4.addWidget(self.gaussian_filter)

        self.median_filter = QFrame(self.filter_cont)
        self.median_filter.setObjectName(u"median_filter")
        self.median_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.median_filter.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_4.addWidget(self.median_filter)

        self.dilate_erode_filter = QFrame(self.filter_cont)
        self.dilate_erode_filter.setObjectName(u"dilate_erode_filter")
        self.dilate_erode_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.dilate_erode_filter.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_4.addWidget(self.dilate_erode_filter)


        self.verticalLayout_3.addWidget(self.filter_cont)

        self.ocr_settings_cont = QFrame(self.control_cont)
        self.ocr_settings_cont.setObjectName(u"ocr_settings_cont")
        self.ocr_settings_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.ocr_settings_cont.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_3.addWidget(self.ocr_settings_cont)


        self.horizontalLayout_2.addWidget(self.control_cont)

        self.text_edit = QTextEdit(self.right_cont)
        self.text_edit.setObjectName(u"text_edit")

        self.horizontalLayout_2.addWidget(self.text_edit)

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
        self.grey_chbx.setText(QCoreApplication.translate("MainWindow", u"To Grey", None))
        self.binarize_chbx.setText(QCoreApplication.translate("MainWindow", u"Binarize", None))
        self.binarize_val_lbl.setText(QCoreApplication.translate("MainWindow", u"100", None))
    # retranslateUi

