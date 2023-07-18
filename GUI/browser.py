import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QMenuBar, QSplitter, QGroupBox, QLabel, QLineEdit, QTextEdit, QAction, QMenu, QPushButton, QFileDialog

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a QVBoxLayout instance
        vbox = QVBoxLayout()

        # Create the menu bar
        menu_bar = QMenuBar()
        vbox.addWidget(menu_bar)

        # Create the file menu
        file_menu = QMenu("File", self)

        # Add filler actions for the file menu
        filler_action1 = QAction("Option 1", self)
        file_menu.addAction(filler_action1)

        filler_action2 = QAction("Option 2", self)
        file_menu.addAction(filler_action2)

        filler_action3 = QAction("Option 3", self)
        file_menu.addAction(filler_action3)

        # Add the file menu to the menu bar
        menu_bar.addMenu(file_menu)

        # Create the splitter
        splitter = QSplitter()
        vbox.addWidget(splitter)

        # Create the form box
        form_box = QGroupBox("Form Box")
        form_layout = QVBoxLayout()
        form_box.setLayout(form_layout)
        splitter.addWidget(form_box)

        # Add widgets to the form box
        label1 = QLabel("Directory 1:")
        line_edit1 = QLineEdit()
        form_layout.addWidget(label1)
        form_layout.addWidget(line_edit1)

        directory_button1 = QPushButton("Browse")
        directory_button1.clicked.connect(lambda: self.browse_directory(line_edit1))
        form_layout.addWidget(directory_button1)

        label2 = QLabel("Directory 2:")
        line_edit2 = QLineEdit()
        form_layout.addWidget(label2)
        form_layout.addWidget(line_edit2)

        directory_button2 = QPushButton("Browse")
        directory_button2.clicked.connect(lambda: self.browse_directory(line_edit2))
        form_layout.addWidget(directory_button2)

        # Set the layout for the main window
        self.setLayout(vbox)

        self.setWindowTitle('Vertical Layout with Frames')
        self.setGeometry(300, 300, 400, 300)
        self.show()

    def browse_directory(self, line_edit):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        line_edit.setText(directory)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())
