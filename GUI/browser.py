import os
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, \
    QSplitter, QSizePolicy


class ImageBrowserWindow(QMainWindow):
    def __init__(self, image_directory):
        super().__init__()
        self.setWindowTitle('Image Browser')
        self.setGeometry(100, 100, 800, 600)

        self.image_directory = image_directory
        self.images = []
        self.current_image_index = 0

        self.image_label_widget = QWidget(self)
        self.image_label_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label_layout = QHBoxLayout(self.image_label_widget)
        self.image_label_layout.setContentsMargins(0, 0, 0, 0)

        self.image_list_widget = QListWidget(self)
        self.image_list_widget.itemClicked.connect(self.show_selected_image)
        self.image_list_widget.setMinimumSize(200,200)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.image_list_widget)
        splitter.addWidget(self.image_label_widget)
        splitter.setSizes([200, 400])
        splitter.setMinimumSize(200,200)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        layout = QHBoxLayout()
        layout.addWidget(splitter)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_images()
        self.populate_image_list()
        self.show_current_image()

    def load_images(self):
        image_files = [file for file in os.listdir(self.image_directory) if file.endswith('.jpg')]
        self.images = [os.path.join(self.image_directory, file) for file in image_files]

    def populate_image_list(self):
        for image_path in self.images:
            image_name = os.path.basename(image_path)
            item = QListWidgetItem(image_name)
            self.image_list_widget.addItem(item)

    def show_selected_image(self, item):
        index = self.image_list_widget.row(item)
        if index != self.current_image_index:
            self.current_image_index = index
            self.show_current_image()

    def show_current_image(self):
        image_path = self.images[self.current_image_index]
        pixmap = QPixmap(image_path)

        image_label = QLabel(self.image_label_widget)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(pixmap.scaled(self.image_label_widget.size(), Qt.AspectRatioMode.KeepAspectRatio))

        if self.image_label_layout.count() > 0:
            self.image_label_layout.itemAt(0).widget().deleteLater()

        self.image_label_layout.addWidget(image_label)

    def eventFilter(self, obj, event):
        if obj == self.image_list_widget and event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Up:
                self.navigate(-1)
                return True
            elif key == Qt.Key_Down:
                self.navigate(1)
                return True
        return super().eventFilter(obj, event)

    def navigate(self, direction):
        new_index = self.current_image_index + direction
        if 0 <= new_index < len(self.images):
            self.current_image_index = new_index
            self.image_list_widget.setCurrentIndex(self.image_list_widget.model().index(new_index, 0))
            self.show_current_image()

    def showEvent(self, event):
        self.image_list_widget.installEventFilter(self)

    def hideEvent(self, event):
        self.image_list_widget.removeEventFilter(self)


if __name__ == '__main__':
    app = QApplication([])
    window = ImageBrowserWindow('test')
    window.show()
    app.exec_()
