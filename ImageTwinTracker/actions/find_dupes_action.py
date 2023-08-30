from PyQt5.QtWidgets import QMessageBox
from ImageTwinTracker.actions.find_dupes import find_dupes
from ImageTwinTracker.actions.create_image_list import create_image_list


def find_dupes_action(main_widget):
    try:
        dir1 = main_widget.dir_line1.text()  # Get the text from the input field
        if not dir1:
            return
        threshold = main_widget.threshold_textbox.text()

        img_list = create_image_list(main_widget)
        results = find_dupes(img_list, int(threshold))

        if results:
            main_widget.images = []
            main_widget.image_list_widget.clear()
            for dupes in results:
                main_widget.image_list_widget.addSpacer()
                main_widget.images.append('')
                for img in dupes:
                    main_widget.image_list_widget.addItem(img.file_path)
                    main_widget.images.append(img.file_path)
            # remove extra spacer
            main_widget.image_list_widget.takeItem(0)
            main_widget.images.pop(0)
        else:
            QMessageBox.information(main_widget, " ", "No duplicate images were found.")
    except Exception as e:
        print(e)
