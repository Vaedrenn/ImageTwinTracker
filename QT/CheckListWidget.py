from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView


class CheckListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Allows ctrl and  shift click selection

    def addItem(self, item_text):
        item = QListWidgetItem(item_text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # Adds checkboxes
        item.setCheckState(Qt.Unchecked)
        QListWidget.addItem(self, item)  # use QListWidget's addItem

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

        # Uncheck all selected items
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_D:
            selected_items = self.selectedItems()
            for item in selected_items:
                item.setCheckState(Qt.Unchecked)

        # do default action
        else:
            super().keyPressEvent(event)
