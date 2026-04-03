import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from utils import get_map_image


class MapApp(QMainWindow):
    def __init__(self, lon, lat, zoom):
        super().__init__()
        self.setWindowTitle("Большая задача по Maps API. Часть №1")
        self.setGeometry(100, 100, 600, 450)
        self.label = QLabel(self)
        self.label.resize(600, 450)
        self.display_map(lon, lat, zoom)

    def display_map(self, lon, lat, zoom):
        image_data = get_map_image(lon, lat, zoom)
        if image_data:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.label.setPixmap(pixmap)
        else:
            self.label.setText("Ошибка загрузки карты")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    longitude = 37.617635
    latitude = 55.755814
    zoom_level = 15
    
    window = MapApp(longitude, latitude, zoom_level)
    window.show()
    sys.exit(app.exec())