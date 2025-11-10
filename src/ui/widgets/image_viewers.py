from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import QEvent, Slot, Qt

from ui.models.image_store import ImageStore
from ui.widgets.custom_image_viewer import ImageViewer
from utils.file_utils import open_file_dialog


class OriginalImageViewer(QFrame):
    def __init__(self, image_store: ImageStore):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self.image_store = image_store
        
        # Listen to image store changes
        self.image_store.imageChanged.connect(self.on_image_changed)
        
        # Top button bar
        self._create_button_bar()
        
        # Image viewer
        self.image_viewer = ImageViewer(self)
        self.layout().addWidget(self.image_viewer)
        
        # Enable drag and drop
        self.image_viewer.setAcceptDrops(True)
        self.image_viewer.installEventFilter(self)
    
    def _create_button_bar(self):
        """Create the top button bar with file chooser."""
        btn_cont = QFrame()
        btn_cont.setFixedHeight(50)
        btn_cont.setLayout(QHBoxLayout())
        
        # Choose image button
        choose_btn = QPushButton("Choose image")
        choose_btn.setCursor(Qt.PointingHandCursor)
        choose_btn.clicked.connect(self.on_choose_image)
        btn_cont.layout().addWidget(choose_btn)
        
        # Instruction label
        label = QLabel("Or drag and drop an image file below")
        btn_cont.layout().addWidget(label)
        
        # Spacer
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        btn_cont.layout().addItem(spacer)
        
        self.layout().addWidget(btn_cont)
    
    # ========================================================================
    # File Loading
    # ========================================================================
    
    @Slot()
    def on_choose_image(self):
        """Open file dialog to choose an image."""
        file_path = open_file_dialog(
            parent=self,
            caption="Choose Image",
            filter_str="Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_path:
            self._load_image(file_path)
    
    def _load_image(self, file_path: str):
        """Load image from file and publish to store."""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            # Display in viewer
            self.image_viewer.load_pixmap(pixmap)
            
            # Publish to store (so other widgets can see it)
            qimage = pixmap.toImage()
            self.image_store.set_original_img(qimage, file_path)
            self.image_store.set_edited_img(qimage)
    
    @Slot(QImage, str)
    def on_image_changed(self, qimg: QImage, path: str):
        """Handle image change from store."""
        pixmap = QPixmap.fromImage(qimg)
        self.image_viewer.load_pixmap(pixmap)
    
    # ========================================================================
    # Drag and Drop
    # ========================================================================
    
    def eventFilter(self, obj, event):
        """Handle drag and drop events."""
        if obj == self.image_viewer:
            if event.type() in (QEvent.DragEnter, QEvent.DragMove):
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                return True
            
            elif event.type() == QEvent.Drop:
                urls = event.mimeData().urls()
                if urls and event.mimeData().hasUrls():
                    file_path = urls[0].toLocalFile()
                    # Validate it's an image
                    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                        self._load_image(file_path)
                        event.acceptProposedAction()
                        return True
                return True
        
        return super().eventFilter(obj, event)


class EditedImageViewer(QFrame):
    def __init__(self, image_store: ImageStore):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.image_store = image_store

        # Store original pixmap for scaling
        self.original_pixmap = None

        # when edited image changes anywhere, show it here as the right panel
        self.image_store.editedImageChanged.connect(self.show_image)

        # Image viewer widget
        self.image_viewer = ImageViewer()
        self.layout().addWidget(self.image_viewer)

    @Slot(QImage)
    def show_image(self, qimg: QImage):
        """Set image on the custom image viewer."""
        if qimg is not None and not qimg.isNull():
            self.original_pixmap = QPixmap.fromImage(qimg)
            self.image_viewer.load_pixmap(self.original_pixmap)
