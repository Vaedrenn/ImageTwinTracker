from PyQt5.QtWidgets import QDialog

from gui.DeletePopUp import DeleteDialog


@staticmethod
class DeleteSelected:
    def delete_selected(main_widget):
        try:
            file_indexes = main_widget.image_list_widget.getCheckedRows()
            files = []

            for f in file_indexes:
                files.append(main_widget.images[f])
            delete_dialog = DeleteDialog(files)
            result = delete_dialog.exec_()

            if result == QDialog.Accepted:
                main_widget.image_list_widget.removeCheckedRows()
                file_indexes.sort(reverse=True)

                for row in file_indexes:
                    main_widget.images.pop(row)

        except Exception as E:
            print("Exception in ImageTwinTracker.delete_selected: ", E)
