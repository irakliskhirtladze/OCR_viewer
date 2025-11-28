from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QMainWindow

from ui.models.image_store import ImageStore
from ui.models.ocr_store import OCRStore
from ui.widgets.editor_panel import EditorContainer
from ui.widgets.image_viewers import EditedImageViewer
from ui.widgets.text_viewer import TextViewerWidget

from ui.generated.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load generated UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("OCR Viewer")
        self.setMinimumSize(QSize(800, 600))
        
        # Create stores
        self.image_store = ImageStore()
        self.ocr_store = OCRStore()
        
        # Initialize widgets with stores
        self._setup_left_container()
        self._setup_right_container()
        
        # Connect signals
        self._connect_signals()
    
    def _setup_left_container(self):
        """Initialize left container widgets."""
        # Inject image_store into the promoted HorizontalThumbnailScrollArea
        self.ui.scrollArea.set_image_store(self.image_store)
        
        # Replace QTextEdit with custom TextViewerWidget
        # Remove the designer's QTextEdit
        self.ui.verticalLayout.removeWidget(self.ui.textEdit)
        self.ui.textEdit.deleteLater()
        
        # Add custom TextViewerWidget
        self.text_viewer = TextViewerWidget(self.ocr_store)
        self.ui.verticalLayout.addWidget(self.text_viewer, 1)  # Stretch factor 1
    
    def _setup_right_container(self):
        """Initialize right container widgets."""
        # Replace placeholder frames with custom widgets
        # Remove frame_3 (editor panel placeholder)
        self.ui.horizontalLayout_2.removeWidget(self.ui.frame_3)
        self.ui.frame_3.deleteLater()
        
        # Remove frame_4 (edited image viewer placeholder)
        self.ui.horizontalLayout_2.removeWidget(self.ui.frame_4)
        self.ui.frame_4.deleteLater()
        
        # Add custom widgets
        self.editor_panel = EditorContainer(self.image_store, self.ocr_store)
        self.ui.horizontalLayout_2.addWidget(self.editor_panel, 1)
        
        self.edited_viewer = EditedImageViewer(self.image_store, self.ocr_store)
        self.ui.horizontalLayout_2.addWidget(self.edited_viewer, 2)
    
    def _connect_signals(self):
        """Connect button signals to slots."""
        # Connect "Choose files" button (pushButton_2)
        self.ui.pushButton_2.clicked.connect(self._on_choose_files)
        
        # Connect "Clear all" button (pushButton)
        self.ui.pushButton.clicked.connect(self._on_clear_all)
    
    @Slot()
    def _on_choose_files(self):
        """Handle Choose files button click."""
        # Delegate to scroll area's file loading logic
        self.ui.scrollArea.on_choose_files()
    
    @Slot()
    def _on_clear_all(self):
        """Handle Clear all button click."""
        self.image_store.clear_images()

        # # Create central widget with layout
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)
        # central_widget.setLayout(QHBoxLayout())
        #
        # # Image store
        # self.image_store = ImageStore()
        # self.ocr_store = OCRStore()
        #
        # # ========================================================================
        # # Left container
        # # ========================================================================
        # self.left_container = QFrame()
        # central_widget.layout().addWidget(self.left_container, 2)
        # self.left_container.setLayout(QVBoxLayout())
        # self.left_container.layout().setContentsMargins(0, 0, 0, 0)
        #
        # self.original_image_viewer = OriginalImageViewer(self.image_store)
        # self.left_container.layout().addWidget(self.original_image_viewer)
        #
        # self.text_viewer = TextViewerWidget(self.ocr_store)
        # self.left_container.layout().addWidget(self.text_viewer, 1)
        #
        # # ========================================================================
        # # right container
        # # ========================================================================
        # self.right_container = QFrame()
        # central_widget.layout().addWidget(self.right_container, 3)
        # self.right_container.setLayout(QHBoxLayout())
        # self.right_container.layout().setContentsMargins(0, 0, 0, 0)
        #
        # self.right_container.layout().addWidget(EditorContainer(self.image_store, self.ocr_store), 1)
        # self.right_container.layout().addWidget(EditedImageViewer(self.image_store, self.ocr_store), 2)
