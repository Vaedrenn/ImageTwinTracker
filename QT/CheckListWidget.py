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

    def addSpacer(self,):
        item = QListWidgetItem()
        # make item not selectable
        item.setFlags(
            item.flags() & ~(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable))  # Clear selectable and checkable flags
        QListWidget.addItem(self, item)  # use QListWidget

    def getCheckedRows(self):
        return self.__getRows(Qt.Checked)

    def getUncheckedRows(self):
        return self.__getRows(Qt.Unchecked)

    def __getRows(self, status: Qt.CheckState):
        ret_list = []
        for i in range(self.count()):
            item = self.item(i)
            if item.checkState() == status:
                ret_list.append(i)

        return ret_list

    def removeCheckedRows(self):
        status = Qt.Checked
        checked_rows = self.__getRows(status)
        checked_rows = reversed(checked_rows)
        for i in checked_rows:
            self.takeItem(i)

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

        # Uncheck all selected items with CTRL + D
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_D:
            selected_items = self.selectedItems()
            for item in selected_items:
                item.setCheckState(Qt.Unchecked)

        # do default action
        else:
            super().keyPressEvent(event)
