from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class PixmapLabel(QLabel):
    mouse_position_signal = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.handle_mouse_movement = False

    def setPixmap(self, pixmap: QPixmap) -> None:
        self.handle_mouse_movement = True
        self.setMouseTracking(True)
        super().setPixmap(pixmap)

    def mouseMoveEvent(self, event):
        if not self.handle_mouse_movement:
            event.ignore()
            return

        event_x = event.pos().x()
        event_y = event.pos().y()
        if event_x < 0 or event_y < 0:
            event.ignore()
            return
        pixmap_height = self.pixmap().size().height()
        pixmap_width = self.pixmap().size().width()
        if event_x > pixmap_width or event_y > pixmap_height:
            event.ignore()
            return

        position_x = (event_x / pixmap_width)
        position_y = (event_y / pixmap_height)
        event.accept()
        self.mouse_position_signal.emit(position_x, position_y)
