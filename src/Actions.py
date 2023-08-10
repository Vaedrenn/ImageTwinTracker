from PyQt5.QtWidgets import QDialog

from src.DeletePopUp import DeleteDialog
from src.find_dupes import create_img_list, find_dupes


class Actions:
    @staticmethod
    def find_dupes_action(main_widget):
        try:
            dir1 = main_widget.dir_line1.text()  # Get the text from the input field
            if not dir1:
                return
            threshold = main_widget.threshold_textbox.text()
            threads = main_widget.preferences.get('Threads')
            img_list = create_img_list(dir1, threads)
            results = find_dupes(img_list, threads, int(threshold))
            if results:
                main_widget.images = []
                main_widget.image_list_widget.clear()
                for dupes in results:
                    for img in dupes:
                        main_widget.image_list_widget.addItem(img.file_path)
                        main_widget.images.append(img.file_path)
                    main_widget.image_list_widget.addSpacer()
                    main_widget.images.append('')
        except Exception as e:
            print(e)

    @staticmethod
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
            print("Exception in Application.delete_selected: ", E)

