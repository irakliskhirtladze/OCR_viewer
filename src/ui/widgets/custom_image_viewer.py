from PySide6.QtGui import QPixmap, Qt, QPainter
from PySide6.QtWidgets import QFrame, QLabel
from PySide6.QtCore import QEvent, QPoint, QTimer


class ImageViewer(QFrame):
    """
    Reusable image viewer widget with pan, zoom, and zoom indicator.
    
    Features:
    - Mouse wheel zoom (zoom to cursor position)
    - Left-click drag to pan (when zoomed in)
    - Zoom indicator overlay
    - Automatic cursor changes (arrow/open hand/closed hand)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: grey;")
        
        # Image state
        self.original_pixmap = None  # Original full-size image
        self.pixmap = None  # Currently displayed (scaled) pixmap
        
        # Pan state
        self.pan_offset = QPoint(0, 0)
        self.last_mouse_pos = None
        self.is_panning = False
        
        # Zoom state
        self.zoom_level = 1.0  # 1.0 = 100% (fit to widget)
        self.min_zoom = 1.0  # Can't zoom out below fit level
        self.max_zoom = 5.0  # 500% max zoom
        self.zoom_step = 0.1  # 10% per wheel step
        
        # Zoom indicator overlay
        self.zoom_label = QLabel(self)
        self.zoom_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 180); color: white; "
            "padding: 5px 10px; border-radius: 3px; font-size: 12px;"
        )
        self.zoom_label.setAlignment(Qt.AlignCenter)
        self.zoom_label.hide()
        self.zoom_label.move(10, 10)
        self.zoom_label.raise_()
        
        # Enable mouse tracking for zoom
        self.installEventFilter(self)
    
    # ========================================================================
    # Public methods
    # ========================================================================
    
    def load_pixmap(self, pixmap: QPixmap):
        """Load a new image and reset zoom/pan."""
        if pixmap is None or pixmap.isNull():
            return
        
        self.original_pixmap = pixmap
        self.zoom_level = 1.0
        self.pan_offset = QPoint(0, 0)
        self._scale_and_display()
        self._update_zoom_indicator()
    
    def clear(self):
        """Clear the displayed image."""
        self.original_pixmap = None
        self.pixmap = None
        self.zoom_level = 1.0
        self.pan_offset = QPoint(0, 0)
        self.update()
    
    # ========================================================================
    # Painting
    # ========================================================================
    
    def paintEvent(self, event):
        """Custom paint to draw pixmap with pan offset."""
        super().paintEvent(event)
        
        if self.pixmap is not None and not self.pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Calculate centered position with pan offset
            x = (self.width() - self.pixmap.width()) // 2 + self.pan_offset.x()
            y = (self.height() - self.pixmap.height()) // 2 + self.pan_offset.y()
            
            painter.drawPixmap(x, y, self.pixmap)
    
    def resizeEvent(self, event):
        """Handle widget resize to rescale the image."""
        super().resizeEvent(event)
        if self.original_pixmap is not None:
            self._scale_and_display()
    
    # ========================================================================
    # Mouse Events - Panning
    # ========================================================================
    
    def mousePressEvent(self, event):
        """Start panning on left mouse button."""
        if event.button() == Qt.LeftButton and self._is_pannable():
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Pan the image while dragging."""
        if self.is_panning and self.last_mouse_pos is not None:
            delta = event.pos() - self.last_mouse_pos
            self.pan_offset += delta
            self._clamp_pan_offset()
            self.last_mouse_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Stop panning."""
        if event.button() == Qt.LeftButton:
            self.is_panning = False
            self.last_mouse_pos = None
            self._update_cursor()
        super().mouseReleaseEvent(event)
    
    def enterEvent(self, event):
        """Handle mouse entering the widget."""
        self._update_cursor()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leaving the widget."""
        if not self.is_panning:
            self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)
    
    # ========================================================================
    # Event Filter - Zooming
    # ========================================================================
    
    def eventFilter(self, obj, event):
        """Handle mouse wheel zoom."""
        if obj == self and event.type() == QEvent.Wheel:
            if self.original_pixmap is not None:
                delta = event.angleDelta().y()
                old_zoom = self.zoom_level
                
                # Calculate new zoom level
                if delta > 0:
                    self.zoom_level = min(self.zoom_level + self.zoom_step, self.max_zoom)
                else:
                    self.zoom_level = max(self.zoom_level - self.zoom_step, self.min_zoom)
                
                # Only update if zoom changed
                if self.zoom_level != old_zoom:
                    if self.zoom_level == 1.0:
                        # Reset to centered when at fit level
                        self.pan_offset = QPoint(0, 0)
                        self._scale_and_display()
                    else:
                        # Zoom towards mouse cursor
                        mouse_pos = event.position().toPoint()
                        self._zoom_at_point(mouse_pos, old_zoom)
                    
                    self._update_zoom_indicator()
                return True
        
        return super().eventFilter(obj, event)
    
    # ========================================================================
    # Internal Helpers
    # ========================================================================
    
    def _is_pannable(self) -> bool:
        """Check if image is pannable (larger than widget)."""
        if self.pixmap is None:
            return False
        return self.pixmap.width() > self.width() or self.pixmap.height() > self.height()
    
    def _update_cursor(self):
        """Update cursor based on whether image is pannable."""
        if not self.is_panning:
            if self._is_pannable():
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
    
    def _scale_and_display(self):
        """Scale the original pixmap based on zoom level and display it."""
        if self.original_pixmap is None:
            return
        
        # Calculate base size (fit to widget)
        base_size = self.original_pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ).size()
        
        # Apply zoom level
        target_width = int(base_size.width() * self.zoom_level)
        target_height = int(base_size.height() * self.zoom_level)
        
        # Scale the pixmap
        self.pixmap = self.original_pixmap.scaled(
            target_width,
            target_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # Clamp pan offset and update cursor
        self._clamp_pan_offset()
        self._update_cursor()
        self.update()
    
    def _zoom_at_point(self, mouse_pos: QPoint, old_zoom: float):
        """Zoom towards a specific point (mouse cursor position)."""
        # Calculate mouse position relative to image center before zoom
        old_center_x = self.width() / 2
        old_center_y = self.height() / 2
        
        rel_x = mouse_pos.x() - old_center_x - self.pan_offset.x()
        rel_y = mouse_pos.y() - old_center_y - self.pan_offset.y()
        
        # Scale the image
        self._scale_and_display()
        
        # Calculate new position to keep the same point under cursor
        zoom_ratio = self.zoom_level / old_zoom
        new_rel_x = rel_x * zoom_ratio
        new_rel_y = rel_y * zoom_ratio
        
        # Adjust pan offset
        self.pan_offset.setX(int(self.pan_offset.x() + (rel_x - new_rel_x)))
        self.pan_offset.setY(int(self.pan_offset.y() + (rel_y - new_rel_y)))
        
        # Clamp and update
        self._clamp_pan_offset()
        self.update()
    
    def _clamp_pan_offset(self):
        """Limit panning to prevent empty space."""
        if self.pixmap is None:
            return
        
        # If image fits entirely, center it
        if self.pixmap.width() <= self.width() and self.pixmap.height() <= self.height():
            self.pan_offset = QPoint(0, 0)
            return
        
        # Calculate excess in each dimension
        excess_x = self.pixmap.width() - self.width()
        excess_y = self.pixmap.height() - self.height()
        
        # Clamp X
        if excess_x > 0:
            max_offset_x = excess_x // 2
            self.pan_offset.setX(max(-max_offset_x, min(max_offset_x, self.pan_offset.x())))
        else:
            self.pan_offset.setX(0)
        
        # Clamp Y
        if excess_y > 0:
            max_offset_y = excess_y // 2
            self.pan_offset.setY(max(-max_offset_y, min(max_offset_y, self.pan_offset.y())))
        else:
            self.pan_offset.setY(0)
    
    def _update_zoom_indicator(self):
        """Update the zoom level indicator overlay."""
        zoom_percent = int(self.zoom_level * 100)
        self.zoom_label.setText(f"{zoom_percent}%")
        self.zoom_label.adjustSize()
        self.zoom_label.show()
        
        # Auto-hide after 5 seconds
        QTimer.singleShot(5000, self.zoom_label.hide)
