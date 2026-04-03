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
        self.setWindowTitle("Большая задача по Maps API. Часть №2")
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
        if event.key() == Qt.Key.Key_PageUp:
            if self.zoom < 21:
                self.zoom += 1
                self.update_map()
        elif event.key() == Qt.Key.Key_PageDown:
            if self.zoom > 0:
                self.zoom -= 1
                self.update_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    longitude = 37.617635
    latitude = 55.755814
    initial_zoom = 10
    window = MapApp(longitude, latitude, initial_zoom)
    window.show()
    sys.exit(app.exec())