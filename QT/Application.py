import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenuBar, QSplitter, QGroupBox, QLabel, \
    QLineEdit, QMenu, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QStyleFactory, QAbstractItemView, QGridLayout, \
    QAction, QListWidgetItem
from dark_palette import create_dark_palette
import CheckListWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        dark_palette = create_dark_palette()
        self.setPalette(dark_palette)

        # Create main layout, put everything here
        vbox = QVBoxLayout()

        # ############################ Menu  ################################ #
        menu_bar = QMenuBar(self)
        menu_bar.setFixedHeight(24)
        vbox.addWidget(menu_bar)

        # Create the file menu
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        options_action = QAction("Options", self)
        file_menu.addAction(options_action)

        clear_cache = QAction("Clear Cache", self)
        file_menu.addAction(clear_cache)

        # ############################ splitter ################################ #
        splitter = QSplitter()
        vbox.addWidget(splitter)
        splitter.setChildrenCollapsible(False)

        # Create the list widget
        list_widget = CheckListWidget.CheckListWidget()
        splitter.addWidget(list_widget)

        # Checklist with dummy vars
        for i in range(50):
            item = QListWidgetItem(f"Item {i + 1}")
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            list_widget.addItem(item)

        # Create a blank image
        image = QImage()

        # Add the image to a label
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image))
        splitter.addWidget(image_label)

        splitter.setSizes([200, 600])

        # ########################## Action Box ################################# #
        action_box = QGroupBox()
        action_box_layout = QHBoxLayout()
        action_box.setLayout(action_box_layout)
        action_box.setFixedHeight(50)
        vbox.addWidget(action_box)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(lambda: None)
        delete_button.setFixedWidth(90)

        spacer = QLabel()

        threshold_label = QLabel("Threshold:")
        threshold_label.setFixedWidth(60)

        threshold_textbox = QLineEdit("200")
        threshold_textbox.setFixedWidth(50)
        threshold_textbox.setMaxLength(5)  # no reason for more than 5 digits
        validator = QIntValidator()  # restrict input to integers
        threshold_textbox.setValidator(validator)  # Set the validator for the line edit

        threshold_button = QPushButton("Find Dupes")
        threshold_button.setFixedWidth(75)
        threshold_button.clicked.connect(lambda: None)

        action_box_layout.addWidget(delete_button)
        action_box_layout.addWidget(spacer)
        action_box_layout.addWidget(threshold_label)
        action_box_layout.addWidget(threshold_textbox)
        action_box_layout.addWidget(threshold_button)

        # ############################# Form Box ################################## #
        form_box = QGroupBox()
        form_box.setFixedHeight(100)
        form_layout = QGridLayout()
        form_box.setLayout(form_layout)
        vbox.addWidget(form_box)

        # Create the first directory lookup
        label1 = QLabel("Directory 1:")
        line_edit1 = QLineEdit()
        directory_button1 = QPushButton("Browse")
        directory_button1.clicked.connect(lambda: self.browse_directory(line_edit1))
        form_layout.addWidget(label1, 0, 0)
        form_layout.addWidget(line_edit1, 0, 1)
        form_layout.addWidget(directory_button1, 0, 2)

        # Create the second directory lookup
        label2 = QLabel("Directory 2:")
        line_edit2 = QLineEdit()
        directory_button2 = QPushButton("Browse")
        directory_button2.clicked.connect(lambda: self.browse_directory(line_edit2))
        form_layout.addWidget(label2, 1, 0)
        form_layout.addWidget(line_edit2, 1, 1)
        form_layout.addWidget(directory_button2, 1, 2)

        # ################################## Set the layout for the main window ################################### #

        self.setLayout(vbox)
        self.setWindowTitle('MSE Duplicate Image Search')
        self.setGeometry(300, 300, 800, 600)
        self.show()

    def browse_directory(self, line_edit):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        line_edit.setText(directory)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())
