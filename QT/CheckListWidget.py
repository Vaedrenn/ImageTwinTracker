import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QAbstractItemView, QApplication


class CheckListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def addCheckBoxItem(self, item_text):
        item = QListWidgetItem(item_text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        self.addItem(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            selected_items = self.selectedItems()
            for item in selected_items:
                item.setCheckState(Qt.Checked)

        # Call the base class implementation to handle other key events
        super().keyPressEvent(event)
