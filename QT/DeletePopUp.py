import os

from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QVBoxLayout, QDialog, QMessageBox
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
        if self.deletefiles(self.files) is False:
            self.reject()
            return QDialog.Rejected
        super().accept()


    def deletefiles(self, files):
        try:
            # fixed file not found error with send2trash
            cleaned = []
            for f in files:
                cleaned.append(os.path.normpath(f))
            send2trash(files)

        except Exception as E:
            self.show_error_message(str(E))
            print("Exception in DeletePopup.deletefiles: ", E)
            return False
        return True

    def show_error_message(self, error_text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText('An exception has occurred:')
        msg.setInformativeText(error_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()