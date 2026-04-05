import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QLineEdit, QVBoxLayout, QHBoxLayout, QWidget)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from utils import get_map_image, geocode


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lon = 37.617635
        self.lat = 55.755814
        self.zoom = 10
        self.theme = "dark"
        self.marker = None

        self.setWindowTitle("Большая задача по Maps API. Часть №5")
        self.setGeometry(100, 100, 600, 550)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск адреса...(хм.....)")
        self.search_input.returnPressed.connect(self.search_object)
        
        self.search_btn = QPushButton("Искать")
        self.search_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.search_btn.clicked.connect(self.search_object)
        
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_btn)
        self.main_layout.addLayout(self.search_layout)

        self.label = QLabel(self)
        self.label.setFixedSize(600, 450)
        self.main_layout.addWidget(self.label)

        self.theme_btn = QPushButton("Сменить тему")
        self.theme_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.theme_btn)

        self.update_map()

    def search_object(self):
        query = self.search_input.text()
        if query:
            pos = geocode(query)
            if pos:
                self.lon, self.lat = pos
                self.marker = pos 
                self.update_map()
                self.setFocus() 

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.update_map()

    def update_map(self):
        image_data = get_map_image(self.lon, self.lat, self.zoom, self.theme, self.marker)
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
        self.update_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec())