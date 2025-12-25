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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

from ui.widgets.common.scroll_area import HorizontalThumbnailScrollArea
from ui.widgets.edited_image_viewer import EditedImageViewer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1088, 776)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.left_cont = QFrame(self.centralwidget)
        self.left_cont.setObjectName(u"left_cont")
        self.left_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.left_cont)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.file_load_cont = QFrame(self.left_cont)
        self.file_load_cont.setObjectName(u"file_load_cont")
        self.file_load_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.file_load_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.file_load_cont)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.button_bar_cont = QFrame(self.file_load_cont)
        self.button_bar_cont.setObjectName(u"button_bar_cont")
        self.button_bar_cont.setMaximumSize(QSize(16777215, 50))
        self.button_bar_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.button_bar_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.button_bar_cont)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.choose_files_btn = QPushButton(self.button_bar_cont)
        self.choose_files_btn.setObjectName(u"choose_files_btn")
        self.choose_files_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.choose_files_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.clear_all_btn = QPushButton(self.button_bar_cont)
        self.clear_all_btn.setObjectName(u"clear_all_btn")
        self.clear_all_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.clear_all_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.button_bar_cont)

        self.thumb_scroll_area = HorizontalThumbnailScrollArea(self.file_load_cont)
        self.thumb_scroll_area.setObjectName(u"thumb_scroll_area")
        self.thumb_scroll_area.setMinimumSize(QSize(0, 150))
        self.thumb_scroll_area.setMaximumSize(QSize(16777215, 150))
        self.thumb_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.thumb_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.thumb_scroll_area.setWidgetResizable(True)
        self.thumb_scroll_widget = QWidget()
        self.thumb_scroll_widget.setObjectName(u"thumb_scroll_widget")
        self.thumb_scroll_widget.setGeometry(QRect(0, 0, 769, 136))
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

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.control_cont = QFrame(self.centralwidget)
        self.control_cont.setObjectName(u"control_cont")
        self.control_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.control_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.control_cont)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.filter_cont = QFrame(self.control_cont)
        self.filter_cont.setObjectName(u"filter_cont")
        self.filter_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.filter_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.filter_cont)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
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

        self.line_2 = QFrame(self.filter_cont)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

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
        self.binarize_slider.setEnabled(False)
        self.binarize_slider.setMaximum(255)
        self.binarize_slider.setValue(127)
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

        self.line_3 = QFrame(self.filter_cont)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_3)

        self.invert_filter = QFrame(self.filter_cont)
        self.invert_filter.setObjectName(u"invert_filter")
        self.invert_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.invert_filter.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.invert_filter)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.invert_chbx = QCheckBox(self.invert_filter)
        self.invert_chbx.setObjectName(u"invert_chbx")

        self.horizontalLayout_6.addWidget(self.invert_chbx)


        self.verticalLayout_4.addWidget(self.invert_filter)

        self.line_4 = QFrame(self.filter_cont)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.median_filter = QFrame(self.filter_cont)
        self.median_filter.setObjectName(u"median_filter")
        self.median_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.median_filter.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.median_filter)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.median_chbx = QCheckBox(self.median_filter)
        self.median_chbx.setObjectName(u"median_chbx")

        self.verticalLayout_7.addWidget(self.median_chbx)

        self.frame_2 = QFrame(self.median_filter)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.median_lbl = QLabel(self.frame_2)
        self.median_lbl.setObjectName(u"median_lbl")

        self.horizontalLayout_7.addWidget(self.median_lbl)

        self.median_ksize_spinbox = QSpinBox(self.frame_2)
        self.median_ksize_spinbox.setObjectName(u"median_ksize_spinbox")
        self.median_ksize_spinbox.setEnabled(False)
        self.median_ksize_spinbox.setMinimum(1)
        self.median_ksize_spinbox.setMaximum(49)
        self.median_ksize_spinbox.setSingleStep(2)
        self.median_ksize_spinbox.setValue(3)

        self.horizontalLayout_7.addWidget(self.median_ksize_spinbox)


        self.verticalLayout_7.addWidget(self.frame_2)


        self.verticalLayout_4.addWidget(self.median_filter)

        self.line_5 = QFrame(self.filter_cont)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_5)

        self.dilate_erode_filter = QFrame(self.filter_cont)
        self.dilate_erode_filter.setObjectName(u"dilate_erode_filter")
        self.dilate_erode_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.dilate_erode_filter.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.dilate_erode_filter)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.dilate_erode_chbx = QCheckBox(self.dilate_erode_filter)
        self.dilate_erode_chbx.setObjectName(u"dilate_erode_chbx")

        self.verticalLayout_6.addWidget(self.dilate_erode_chbx)

        self.frame_3 = QFrame(self.dilate_erode_filter)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.dilate_radio = QRadioButton(self.frame_5)
        self.dilate_radio.setObjectName(u"dilate_radio")
        self.dilate_radio.setEnabled(False)
        self.dilate_radio.setChecked(True)

        self.verticalLayout_8.addWidget(self.dilate_radio)

        self.erode_radio = QRadioButton(self.frame_5)
        self.erode_radio.setObjectName(u"erode_radio")
        self.erode_radio.setEnabled(False)

        self.verticalLayout_8.addWidget(self.erode_radio)


        self.horizontalLayout_8.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")

        self.verticalLayout_9.addWidget(self.label)

        self.dilate_erode_ksize_spinbox = QSpinBox(self.frame_4)
        self.dilate_erode_ksize_spinbox.setObjectName(u"dilate_erode_ksize_spinbox")
        self.dilate_erode_ksize_spinbox.setEnabled(False)
        self.dilate_erode_ksize_spinbox.setMinimum(1)
        self.dilate_erode_ksize_spinbox.setMaximum(50)
        self.dilate_erode_ksize_spinbox.setValue(2)

        self.verticalLayout_9.addWidget(self.dilate_erode_ksize_spinbox)


        self.horizontalLayout_8.addWidget(self.frame_4)

        self.frame_6 = QFrame(self.frame_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_2 = QLabel(self.frame_6)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_10.addWidget(self.label_2)

        self.dilate_erode_iter_spinbox = QSpinBox(self.frame_6)
        self.dilate_erode_iter_spinbox.setObjectName(u"dilate_erode_iter_spinbox")
        self.dilate_erode_iter_spinbox.setEnabled(False)
        self.dilate_erode_iter_spinbox.setMinimum(1)
        self.dilate_erode_iter_spinbox.setMaximum(40)

        self.verticalLayout_10.addWidget(self.dilate_erode_iter_spinbox)


        self.horizontalLayout_8.addWidget(self.frame_6)


        self.verticalLayout_6.addWidget(self.frame_3)


        self.verticalLayout_4.addWidget(self.dilate_erode_filter)

        self.line_6 = QFrame(self.filter_cont)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_6)

        self.frame_13 = QFrame(self.filter_cont)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_4)

        self.apply_to_all_btn = QPushButton(self.frame_13)
        self.apply_to_all_btn.setObjectName(u"apply_to_all_btn")
        self.apply_to_all_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_12.addWidget(self.apply_to_all_btn)

        self.reset_all_btn = QPushButton(self.frame_13)
        self.reset_all_btn.setObjectName(u"reset_all_btn")
        self.reset_all_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_12.addWidget(self.reset_all_btn)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addWidget(self.frame_13)


        self.verticalLayout_3.addWidget(self.filter_cont)

        self.ocr_settings_cont = QFrame(self.control_cont)
        self.ocr_settings_cont.setObjectName(u"ocr_settings_cont")
        self.ocr_settings_cont.setFrameShape(QFrame.Shape.StyledPanel)
        self.ocr_settings_cont.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.ocr_settings_cont)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer)

        self.frame_10 = QFrame(self.ocr_settings_cont)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.frame_11 = QFrame(self.frame_10)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_11)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_5 = QLabel(self.frame_11)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_13.addWidget(self.label_5)

        self.ocr_engine_combo = QComboBox(self.frame_11)
        self.ocr_engine_combo.addItem("")
        self.ocr_engine_combo.addItem("")
        self.ocr_engine_combo.setObjectName(u"ocr_engine_combo")

        self.verticalLayout_13.addWidget(self.ocr_engine_combo)


        self.horizontalLayout_11.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.frame_10)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_12)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_6 = QLabel(self.frame_12)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_14.addWidget(self.label_6)

        self.lang_combo = QComboBox(self.frame_12)
        self.lang_combo.setObjectName(u"lang_combo")

        self.verticalLayout_14.addWidget(self.lang_combo)


        self.horizontalLayout_11.addWidget(self.frame_12)


        self.verticalLayout_12.addWidget(self.frame_10)

        self.frame_9 = QFrame(self.ocr_settings_cont)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.run_ocr_btn = QPushButton(self.frame_9)
        self.run_ocr_btn.setObjectName(u"run_ocr_btn")
        self.run_ocr_btn.setEnabled(False)
        self.run_ocr_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_10.addWidget(self.run_ocr_btn)

        self.horizontalSpacer_5 = QSpacerItem(92, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)


        self.verticalLayout_12.addWidget(self.frame_9)

        self.frame_7 = QFrame(self.ocr_settings_cont)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.bboxes_chbox = QCheckBox(self.frame_7)
        self.bboxes_chbox.setObjectName(u"bboxes_chbox")
        self.bboxes_chbox.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.bboxes_chbox)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.avg_conf_lbl = QLabel(self.frame_7)
        self.avg_conf_lbl.setObjectName(u"avg_conf_lbl")

        self.horizontalLayout_2.addWidget(self.avg_conf_lbl)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.export_pdf_btn = QPushButton(self.frame_7)
        self.export_pdf_btn.setObjectName(u"export_pdf_btn")
        self.export_pdf_btn.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.export_pdf_btn)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.verticalLayout_12.addWidget(self.frame_7)


        self.verticalLayout_3.addWidget(self.ocr_settings_cont)


        self.horizontalLayout.addWidget(self.control_cont)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.choose_files_btn.setText(QCoreApplication.translate("MainWindow", u"Choose files", None))
        self.clear_all_btn.setText(QCoreApplication.translate("MainWindow", u"Clear all", None))
        self.grey_chbx.setText(QCoreApplication.translate("MainWindow", u"Grayscale", None))
        self.binarize_chbx.setText(QCoreApplication.translate("MainWindow", u"Binarize", None))
        self.binarize_val_lbl.setText(QCoreApplication.translate("MainWindow", u"127", None))
        self.invert_chbx.setText(QCoreApplication.translate("MainWindow", u"Invert colors", None))
        self.median_chbx.setText(QCoreApplication.translate("MainWindow", u"Median blur", None))
        self.median_lbl.setText(QCoreApplication.translate("MainWindow", u"K size", None))
        self.dilate_erode_chbx.setText(QCoreApplication.translate("MainWindow", u"Dilate/Erode", None))
        self.dilate_radio.setText(QCoreApplication.translate("MainWindow", u"Dilate", None))
        self.erode_radio.setText(QCoreApplication.translate("MainWindow", u"Erode", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"K size", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Iteration", None))
        self.apply_to_all_btn.setText(QCoreApplication.translate("MainWindow", u"Apply filters to all", None))
        self.reset_all_btn.setText(QCoreApplication.translate("MainWindow", u"Reset filters for all", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Choose OCR engine", None))
        self.ocr_engine_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Tesseract", None))
        self.ocr_engine_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"EasyOCR", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Language", None))
        self.run_ocr_btn.setText(QCoreApplication.translate("MainWindow", u"Run OCR", None))
        self.bboxes_chbox.setText(QCoreApplication.translate("MainWindow", u"OCR overlay", None))
        self.avg_conf_lbl.setText("")
        self.export_pdf_btn.setText(QCoreApplication.translate("MainWindow", u"Export PDF", None))
    # retranslateUi

