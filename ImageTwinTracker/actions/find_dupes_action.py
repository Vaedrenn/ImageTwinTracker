from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from actions.find_dupes import create_img_list, find_dupes


class FindDuplicates:
    class WorkerThread(QThread):
        progress_updated = pyqtSignal(int)
        finished_with_results = pyqtSignal(object)  # Define a custom signal with the expected arguments

        def __init__(self, parent=None):
            super().__init__(parent)
            self.dir1 = None
            self.threads = None
            self.threshold = None

        def setup(self, dir1, threads, threshold):
            self.dir1 = dir1
            self.threads = threads
            self.threshold = threshold

        def run(self):
            img_list = create_img_list(self.dir1, self.threads)
            self.progress_updated.emit(50)  # You can adjust this value as needed
            results = find_dupes(img_list, self.threads, self.threshold)
            self.progress_updated.emit(100)
            self.finished_with_results.emit(results)  # Emit the custom signal with the results

    @staticmethod
    def find_dupes_action(main_widget):
        try:
            dir1 = main_widget.dir_line1.text()
            if not dir1:
                return

            threshold = int(main_widget.threshold_textbox.text())
            threads = main_widget.preferences.get('Threads')

            thread = FindDuplicates.WorkerThread()
            thread.setup(dir1, threads, threshold)

            progress_dialog = QProgressDialog("Finding Duplicates...", "Cancel", 0, 100, main_widget)
            progress_dialog.setWindowModality(Qt.WindowModal)

            thread.progress_updated.connect(progress_dialog.setValue)
            thread.finished_with_results.connect(lambda results: FindDuplicates.process_results(main_widget, results))

            progress_dialog.canceled.connect(thread.quit)
            progress_dialog.canceled.connect(thread.wait)

            thread.start()
            progress_dialog.exec_()
        except Exception as e:
            print(e)

    @staticmethod
    def process_results(main_widget, results):
        try:
            if results:
                main_widget.images = []
                main_widget.image_list_widget.clear()
                for dupes in results:
                    main_widget.image_list_widget.addSpacer()
                    main_widget.images.append('')
                    for img in dupes:
                        main_widget.image_list_widget.addItem(img.file_path)
                        main_widget.images.append(img.file_path)
                main_widget.image_list_widget.takeItem(0)
                main_widget.images.pop(0)

        except Exception as e:
            print(e)
