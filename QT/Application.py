import json
import os
import sys
import CheckListWidget
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QImage, QPixmap, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenuBar, QSplitter, QGroupBox, QLabel, \
    QLineEdit, QMenu, QPushButton, QFileDialog, QHBoxLayout, QStyleFactory, QGridLayout, QAction, QListWidgetItem, \
    QSizePolicy


from QT.Options import OptionsDialog
from SearchMse.find_dupes import find_dupes, create_img_list
from light_palette import create_light_palette
from dark_palette import create_dark_palette


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Define the class attributes for input fields
        self.threshold_textbox = None
        self.dir_line1 = None

        # Define the class attributes for splitter widgets
        self.image_list_widget = None
        self.image_label = None
        self.images = []
        self.current_image_index = 0

        self.preferences = {}  # Store preferences as a class attribute
        self.load_preferences()  # Load preferences from the file
        self.initUI()

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        if self.preferences.get('Dark') is True:
            dark_palette = create_dark_palette()
            self.setPalette(dark_palette)
        else:
            light_palette = create_light_palette()
            self.setPalette(light_palette)

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
        options_action.triggered.connect(self.show_options_dialog)
        file_menu.addAction(options_action)

        clear_cache = QAction("Clear Cache", self)
        file_menu.addAction(clear_cache)

        # ############################ splitter ################################ #
        splitter = QSplitter()
        vbox.addWidget(splitter)
        splitter.setChildrenCollapsible(False)

        # Image label
        self.image_label_widget = QWidget(self)
        # make the label expand on resize
        self.image_label_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label_layout = QHBoxLayout(self.image_label_widget)
        self.image_label_layout.setContentsMargins(0, 0, 0, 0)

        # The image list
        self.image_list_widget = CheckListWidget.CheckListWidget()
        self.image_list_widget.itemClicked.connect(self.show_selected_image)  # on click change image

        splitter.addWidget(self.image_list_widget)
        splitter.addWidget(self.image_label_widget)
        splitter.setSizes([200, 600])

        # ########################## Action Box ################################# #
        action_box = QGroupBox()
        action_box_layout = QHBoxLayout()
        action_box.setLayout(action_box_layout)
        action_box.setFixedHeight(50)
        vbox.addWidget(action_box)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(lambda: self.delete_selected())
        delete_button.setFixedWidth(90)

        spacer = QLabel()

        threshold_label = QLabel("Threshold:")
        threshold_label.setFixedWidth(60)

        self.threshold_textbox = QLineEdit("200")
        self.threshold_textbox.setFixedWidth(50)
        self.threshold_textbox.setMaxLength(5)  # no reason for more than 5 digits
        validator = QIntValidator()  # restrict input to integers
        self.threshold_textbox.setValidator(validator)  # Set the validator for the line edit

        threshold_button = QPushButton("Find Dupes")
        threshold_button.setFixedWidth(75)
        threshold_button.clicked.connect(lambda: self.find_dupes_action())

        action_box_layout.addWidget(delete_button)
        action_box_layout.addWidget(spacer)
        action_box_layout.addWidget(threshold_label)
        action_box_layout.addWidget(self.threshold_textbox)
        action_box_layout.addWidget(threshold_button)

        # ############################# Form Box ################################## #
        form_box = QGroupBox()
        form_box.setFixedHeight(100)
        form_layout = QGridLayout()
        form_box.setLayout(form_layout)
        vbox.addWidget(form_box)

        # Create the first directory lookup
        label1 = QLabel("Directory 1:")
        self.dir_line1 = QLineEdit(r"C:\Users\khei\PycharmProjects\MSE-Duplicate-Search\Test_images\Dupe test")  # Make it a class attribute using "self."
        directory_button1 = QPushButton("Browse")
        directory_button1.clicked.connect(lambda: self.browse_directory(self.dir_line1))
        form_layout.addWidget(label1, 0, 0)
        form_layout.addWidget(self.dir_line1, 0, 1)
        form_layout.addWidget(directory_button1, 0, 2)

        """
        # Create the second directory lookup
        label2 = QLabel("Directory 2:")
        self.dir_line2 = QLineEdit()  # Make it a class attribute using "self."
        self.dir_line2.setPlaceholderText(" Leave blank for single directory lookup")
        directory_button2 = QPushButton("Browse")
        directory_button2.clicked.connect(lambda: self.browse_directory(self.dir_line2))
        form_layout.addWidget(label2, 1, 0)
        form_layout.addWidget(self.dir_line2, 1, 1)
        form_layout.addWidget(directory_button2, 1, 2)
        """

        # ################################## Set the layout for the main window ################################### #

        self.setLayout(vbox)
        self.setWindowTitle('MSE Duplicate Image Search')
        self.setGeometry(300, 300, 800, 600)
        self.show()
    def load_preferences(self):
        try:
            with open('pref.json', 'r') as file:
                self.preferences = json.load(file)
        except FileNotFoundError:
            print("Creating preferences file")
            # If the preferences file doesn't exist, create a default set of preferences
            self.preferences = {
                'Threads': 1,
                'CUDA': False,
                'VRAM': 1024,
                'Dark': True,
                # Add more preferences as needed
            }
            with open("pref.json", "w") as file:
                json.dump(self.preferences, file, indent=4)
    def show_options_dialog(self):
        options_dialog = OptionsDialog(self.preferences)
        options_dialog.setWindowTitle("Options")
        options_dialog.exec_()

    def browse_directory(self, line_edit):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        line_edit.setText(directory)

    def find_dupes_action(self):
        dir1 = self.dir_line1.text()  # Get the text from the input field
        if not dir1:
            return
        #dir2 = self.dir_line2.text()  # Get the text from the input field
        threshold = self.threshold_textbox.text()
        # Get the text from the input field
        threads = self.preferences.get('Threads')
        img_list = create_img_list(dir1, threads)

        results = find_dupes(img_list, threads, int(threshold))
        if results:
            self.image_list_widget.clear()
            for dupes in results:
                for img in dupes:
                    self.image_list_widget.addItem(img.file_path)
                    self.images.append(img.file_path)
                self.image_list_widget.addSpacer()
                self.images.append(None)

    def delete_selected(self):
        file_list = self.list_widget.getCheckedRows()
        for file in file_list:
            if os.path.isfile(file):
                # delete.deletefile(file)
                pass
        # remove rows from list_widget
        self.list_widget.removeCheckedRows()

    def show_selected_image(self, item):
        index = self.image_list_widget.row(item)
        if index != self.current_image_index:
            self.current_image_index = index
            print(index)
            image_path = self.images[self.current_image_index]
            print(image_path)
            if image_path is not None:
                try:
                    self.updateImage(image_path)
                except Exception as e: print(e)

    def updateImage(self, path):
        try:
            image_path = self.images[self.current_image_index]
            pixmap = QPixmap(image_path)  # open image as pixmap

            # remove any previous image labels and add new QLabel current image, This prevents stacking of image labels
            while self.image_label_layout.count() > 0:
                self.image_label_layout.takeAt(0).widget().deleteLater()

            image_label = QLabel(self.image_label_widget)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setPixmap(pixmap.scaled(self.image_label_widget.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.image_label_layout.addWidget(image_label)

        except Exception as e: print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec())
