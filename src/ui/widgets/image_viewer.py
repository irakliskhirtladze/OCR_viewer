from PySide6.QtGui import QPixmap, Qt, QPainter
from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import QEvent, QPoint, QTimer

from utils.file_utils import open_file_dialog


class PannableImageWidget(QFrame):
    """Custom widget that displays an image with panning support."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = None
        self.pan_offset = QPoint(0, 0)
        self.last_mouse_pos = None
        self.is_panning = False
        
    def set_pixmap(self, pixmap: QPixmap):
        """Set the pixmap to display."""
        self.pixmap = pixmap
        self.update_cursor()
        self.update()
    
    def paintEvent(self, event):
        """Custom paint to draw pixmap with pan offset."""
        super().paintEvent(event)
        
        if self.pixmap is not None and not self.pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Calculate centered position
            x = (self.width() - self.pixmap.width()) // 2 + self.pan_offset.x()
            y = (self.height() - self.pixmap.height()) // 2 + self.pan_offset.y()
            
            painter.drawPixmap(x, y, self.pixmap)

    def is_pannable(self) -> bool:
        """Check if image is pannable (larger than widget)."""
        if self.pixmap is None:
            return False
        return self.pixmap.width() > self.width() or self.pixmap.height() > self.height()
    
    def update_cursor(self):
        """Update cursor based on whether image is pannable."""
        if not self.is_panning:
            if self.is_pannable():
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
    
    def enterEvent(self, event):
        """Handle mouse entering the widget."""
        self.update_cursor()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leaving the widget."""
        if not self.is_panning:
            self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Start panning on left mouse button."""
        if event.button() == Qt.LeftButton and self.is_pannable():
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Pan the image while dragging."""
        if self.is_panning and self.last_mouse_pos is not None:
            delta = event.pos() - self.last_mouse_pos
            self.pan_offset += delta
            
            # Clamp pan offset to prevent panning too far
            self.clamp_pan_offset()
            
            self.last_mouse_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Stop panning."""
        if event.button() == Qt.LeftButton:
            self.is_panning = False
            self.last_mouse_pos = None
            self.update_cursor()
        super().mouseReleaseEvent(event)
    
    def clamp_pan_offset(self):
        """Limit panning to prevent empty space."""
        if self.pixmap is None:
            return
        
        # If image is smaller than widget, center it (no panning)
        if self.pixmap.width() <= self.width() and self.pixmap.height() <= self.height():
            self.pan_offset = QPoint(0, 0)
            return
        
        # Calculate how much the image exceeds the widget size
        excess_x = self.pixmap.width() - self.width()
        excess_y = self.pixmap.height() - self.height()
        
        # Clamp each dimension independently to prevent empty space
        if excess_x > 0:
            max_offset_x = excess_x // 2
            self.pan_offset.setX(max(-max_offset_x, min(max_offset_x, self.pan_offset.x())))
        else:
            self.pan_offset.setX(0)
        
        if excess_y > 0:
            max_offset_y = excess_y // 2
            self.pan_offset.setY(max(-max_offset_y, min(max_offset_y, self.pan_offset.y())))
        else:
            self.pan_offset.setY(0)


class ImageViewerWidget(QFrame):
    """Widget to display an image. Supports file dialog and image drop to display; Zoom in and out; Pan; Reset view"""

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: grey;")

        # button and text container
        self.btn_cont = QFrame()
        self.btn_cont.setFixedHeight(50)
        self.btn_cont.setLayout(QHBoxLayout())

        self.choose_img_btn = QPushButton("Choose image")
        self.choose_img_btn.setCursor(Qt.PointingHandCursor)
        self.choose_img_btn.clicked.connect(self.on_choose_image)
        self.btn_cont.layout().addWidget(self.choose_img_btn)

        self.text_label = QLabel("Or drag and drop an image file below")
        self.btn_cont.layout().addWidget(self.text_label)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_cont.layout().addItem(spacer)

        self.layout().addWidget(self.btn_cont)

        # Custom widget for panning support
        self.image_container = PannableImageWidget(self)
        self.layout().addWidget(self.image_container)

        # Zoom indicator label
        self.zoom_label = QLabel(self.image_container)
        self.zoom_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 180); color: white; "
            "padding: 5px 10px; border-radius: 3px; font-size: 12px;"
        )
        self.zoom_label.setAlignment(Qt.AlignCenter)
        self.zoom_label.hide()
        self.zoom_label.move(10, 10)  # Top-left corner
        self.zoom_label.raise_()  # Keep on top

        # Store original pixmap and zoom level
        self.original_pixmap = None
        self.zoom_level = 1.0  # 1.0 = 100% (fit to container)
        self.min_zoom = 1.0  # 100% - can't zoom out below fit level
        self.max_zoom = 5.0  # 500%
        self.zoom_step = 0.1  # 10% per wheel step

        # Enable drag and drop and events on image container
        self.image_container.setAcceptDrops(True)
        self.image_container.installEventFilter(self)

    def on_choose_image(self):
        """Open file dialog to choose an image and display it."""
        file_path = open_file_dialog(
            parent=self,
            caption="Choose Image",
            filter_str="Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_path is not None:
            self.load_image(file_path)
    
    def load_image(self, file_path: str):
        """Load and display an image, scaled to fit the container."""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.original_pixmap = pixmap
            self.zoom_level = 1.0  # Reset zoom when loading new image
            self.image_container.pan_offset = QPoint(0, 0)  # Reset pan
            self.scale_image()
            self.update_zoom_indicator()

    def eventFilter(self, obj, event):
        """Filter events for image_container to handle drag and drop and zoom."""
        if obj == self.image_container:
            if event.type() == QEvent.Wheel:
                if self.original_pixmap is not None:
                    # Get wheel delta (positive = zoom in, negative = zoom out)
                    delta = event.angleDelta().y()
                    old_zoom = self.zoom_level
                    
                    # Get mouse position before zoom
                    mouse_pos = event.position().toPoint()
                    
                    if delta > 0:
                        self.zoom_level = min(self.zoom_level + self.zoom_step, self.max_zoom)
                    else:
                        self.zoom_level = max(self.zoom_level - self.zoom_step, self.min_zoom)
                    
                    # Only update if zoom actually changed
                    if self.zoom_level != old_zoom:
                        # Reset pan offset when zooming back to fit level (100%)
                        if self.zoom_level == 1.0:
                            self.image_container.pan_offset = QPoint(0, 0)
                            self.scale_image()
                        else:
                            # Zoom towards mouse cursor
                            self.zoom_at_point(mouse_pos, old_zoom)
                        
                        self.update_zoom_indicator()
                    return True
            
            elif event.type() in (QEvent.DragEnter, QEvent.DragMove):
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                return True
            
            elif event.type() == QEvent.Drop:
                urls = event.mimeData().urls()
                if urls and event.mimeData().hasUrls():
                    file_path = urls[0].toLocalFile()
                    # Validate it's an image
                    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                        self.load_image(file_path)
                        event.acceptProposedAction()
                        return True
                return True
        
        return super().eventFilter(obj, event)
    
    def scale_image(self):
        """Scale the original pixmap to fit the container while maintaining aspect ratio."""
        if self.original_pixmap is not None:
            # Calculate base size (fit to container)
            base_size = self.original_pixmap.scaled(
                self.image_container.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ).size()
            
            # Apply zoom level
            target_width = int(base_size.width() * self.zoom_level)
            target_height = int(base_size.height() * self.zoom_level)
            
            scaled_pixmap = self.original_pixmap.scaled(
                target_width,
                target_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_container.set_pixmap(scaled_pixmap)
            # Clamp pan offset to prevent empty space after zoom
            self.image_container.clamp_pan_offset()
    
    def zoom_at_point(self, mouse_pos: QPoint, old_zoom: float):
        """Zoom towards a specific point (mouse cursor position)."""
        # Calculate the point in image coordinates before zoom
        # Image center position in widget coordinates
        old_center_x = self.image_container.width() / 2
        old_center_y = self.image_container.height() / 2
        
        # Mouse position relative to image center (before zoom)
        rel_x = mouse_pos.x() - old_center_x - self.image_container.pan_offset.x()
        rel_y = mouse_pos.y() - old_center_y - self.image_container.pan_offset.y()
        
        # Scale the image
        self.scale_image()
        
        # Calculate new position to keep the same point under the cursor
        # The relative position scales with zoom ratio
        zoom_ratio = self.zoom_level / old_zoom
        new_rel_x = rel_x * zoom_ratio
        new_rel_y = rel_y * zoom_ratio
        
        # Adjust pan offset to keep the point stationary
        self.image_container.pan_offset.setX(
            int(self.image_container.pan_offset.x() + (rel_x - new_rel_x))
        )
        self.image_container.pan_offset.setY(
            int(self.image_container.pan_offset.y() + (rel_y - new_rel_y))
        )
        
        # Clamp again after adjustment
        self.image_container.clamp_pan_offset()
        self.image_container.update()
    
    def update_zoom_indicator(self):
        """Update the zoom level indicator."""
        zoom_percent = int(self.zoom_level * 100)
        self.zoom_label.setText(f"{zoom_percent}%")
        self.zoom_label.adjustSize()
        self.zoom_label.show()
        
        # Auto-hide after 5 seconds
        QTimer.singleShot(5000, self.zoom_label.hide)
    
    def resizeEvent(self, event):
        """Handle widget resize to rescale the image."""
        super().resizeEvent(event)
        self.scale_image()

