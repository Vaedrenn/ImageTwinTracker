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
        # on space key press swap states
        if event.key() == Qt.Key_Space:
            selected_items = self.selectedItems()
            for item in selected_items:
                current_state = item.checkState()
                if current_state == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
