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

        self.init_ui()
        self.update_map()

    def init_ui(self):
        self.setWindowTitle("Maps API Task")
        self.setGeometry(100, 100, 600, 620)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        search_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите адрес...")
        self.search_input.returnPressed.connect(self.handle_search)

        btn_search = QPushButton("Найти")
        btn_search.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        btn_search.clicked.connect(self.handle_search)

        btn_reset = QPushButton("Сброс")
        btn_reset.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        btn_reset.clicked.connect(self.reset_search)

        search_bar.addWidget(self.search_input)
        search_bar.addWidget(btn_search)
        search_bar.addWidget(btn_reset)
        self.layout.addLayout(search_bar)

        self.address_label = QLabel("Адрес появится здесь")
        self.address_label.setWordWrap(True)
        self.address_label.setStyleSheet(
            "background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;"
        )
        self.layout.addWidget(self.address_label)

        self.map_label = QLabel()
        self.map_label.setFixedSize(600, 450)
        self.layout.addWidget(self.map_label)

        self.btn_theme = QPushButton("Сменить тему")
        self.btn_theme.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_theme.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.btn_theme)

    def handle_search(self):
        query = self.search_input.text().strip()
        if query:
            pos, address = geocode(query)
            if pos:
                self.lon, self.lat = pos
                self.marker = pos
                self.address_label.setText(address)
                self.update_map()
            else:
                self.address_label.setText("Ничего не найдено")
        self.setFocus()

    def reset_search(self):
        self.marker = None
        self.search_input.clear()
        self.address_label.setText("Адрес появится здесь")
        self.update_map()
        self.setFocus()

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.update_map()

    def update_map(self):
        image_data = get_map_image(self.lon, self.lat, self.zoom,
                                   self.theme, self.marker)
        if image_data:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.map_label.setPixmap(pixmap)

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
        self.lon = max(-180, min(180, self.lon))
        self.lat = max(-85, min(85, self.lat))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec())