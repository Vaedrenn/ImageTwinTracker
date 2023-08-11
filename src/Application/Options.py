import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QCheckBox, QLabel, QLineEdit, QDialogButtonBox, QVBoxLayout, QDialog


class OptionsDialog(QDialog):
    def __init__(self, preferences):
        super().__init__()
        self.preferences = preferences
        self.initUI()

    def initUI(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()

        # Create QLabel for the "Threads" option
        threads_label = QLabel("Number of Threads:")
        layout.addWidget(threads_label)

        # Create QLineEdit for the "Threads" option
        threads_entry = QLineEdit()
        threads_entry.setValidator(QIntValidator(1, 12))  # Set the validator for 2-digit integers
        threads_entry.setText(str(self.preferences.get('Threads', 1)))
        layout.addWidget(threads_entry)

        # Create QCheckBox for the "Dark Theme" option
        dark_theme_checkbox = QCheckBox("Dark Theme")
        dark_theme_checkbox.setObjectName("DarkThemeCheckbox")  # Set object name for identification
        dark_theme_checkbox.setChecked(self.preferences.get('Dark'))
        layout.addWidget(dark_theme_checkbox)

        # Add a button box to accept/cancel changes
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        # Save the changes when the user clicks "Ok"
        threads_entry = self.findChild(QLineEdit)
        threads_value = threads_entry.text()
        if threads_value.isdigit():
            self.preferences['Threads'] = int(threads_value)

        dark_theme_checkbox = self.findChild(QCheckBox, "DarkThemeCheckbox")
        self.preferences['Dark'] = dark_theme_checkbox.isChecked()

        # Save the preferences to the file
        with open('../pref.json', 'w') as file:
            json.dump(self.preferences, file, indent=4)

        super().accept()

