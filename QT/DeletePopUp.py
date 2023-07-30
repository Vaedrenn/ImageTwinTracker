from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt
from send2trash import send2trash



class DeleteDialog(QDialog):
    def __init__(self, files):
        super().__init__()
        self.files = files
        self.initUI()

    def initUI(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Deleting Items')
        layout = QVBoxLayout()
        file_count = len(self.files)

        # Create QLabel for the "Threads" option
        label = "Deleting "+str(file_count)+" files continue?"
        text_label = QLabel(label)
        text_label.setAlignment(Qt.AlignCenter)  # Align text to center

        layout.addWidget(text_label)

        # Add a button box to accept/cancel changes
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        self.deletefiles(self.files)
        super().accept()

    def deletefiles(self, files):
        try:
            # remove whatever this is
            raw_files = [f.replace(r'\\\\?\\', '') for f in files]
            # Delete the files using send2trash
            for f in raw_files:
                send2trash(f)
        except Exception as E:
            print(E)
