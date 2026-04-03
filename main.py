import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from utils import get_map_image


class MapApp(QMainWindow):
    def __init__(self, lon, lat, zoom):
        super().__init__()
        self.lon = lon
        self.lat = lat
        self.zoom = zoom
        self.setWindowTitle("Большая задача по Maps API. Часть №3")
        self.setGeometry(100, 100, 600, 450)
        self.label = QLabel(self)
        self.label.resize(600, 450)
        self.update_map()

    def update_map(self):
        image_data = get_map_image(self.lon, self.lat, self.zoom)
        if image_data:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        step = 0.005 * (2 ** (15 - self.zoom))

        if event.key() == Qt.Key.Key_PageUp:
            if self.zoom < 21:
                self.zoom += 1
        elif event.key() == Qt.Key.Key_PageDown:
            if self.zoom > 0:
                self.zoom -= 1
        
        elif event.key() == Qt.Key.Key_Left:
            self.lon -= step
        elif event.key() == Qt.Key.Key_Right:
            self.lon += step
        elif event.key() == Qt.Key.Key_Up:
            self.lat += step
        elif event.key() == Qt.Key.Key_Down:
            self.lat -= step
        else:
            return

        self.check_borders()
        self.update_map()

    def check_borders(self):
        if self.lon > 180:
            self.lon = 180
        elif self.lon < -180:
            self.lon = -180
            
        if self.lat > 85:
            self.lat = 85
        elif self.lat < -85:
            self.lat = -85


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp(37.617635, 55.755814, 10)
    window.show()
    sys.exit(app.exec())