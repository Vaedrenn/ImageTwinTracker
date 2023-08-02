import os
import sys
from unittest import TestCase

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QLineEdit, QMenu, QAction, QSplitter, QPushButton

from GUI.CheckListWidget import CheckListWidget
from SearchMse.find_dupes import create_img_list, find_dupes
from GUI import Application


class TestCreate(TestCase):

    # Test if exactly 11 objects are created
    def test_len(self):
        root = r"Dupe test/Complex 3"
        if not root:
            self.fail("Directory not found")
        img_list = create_img_list(root, 2)
        landscape = img_list[0]
        portrait = img_list[1]

        self.assertEqual(len(landscape), 11)
        self.assertEqual(len(set(landscape)), 11)
        """
        print("landscape")
        for img in landscape:
            img.display_path()
        print("portrait")
        for img in portrait:
            img.display_path()
        """

    # Test if the program accepts invalid files
    def test_valid(self):
        root = r"Tensor test/test 2"
        if not root:
            self.fail("Directory not found")
        img_list = create_img_list(root, 2)
        landscape = img_list[0]
        portrait = img_list[1]
        dud = r"Tensor test/test 2/dud.txt"

        self.assertFalse(dud in landscape)
        self.assertFalse(dud in portrait)


class TestSearch(TestCase):
    # Test if mse search actually detects duplicates
    def test_dupes(self, threshold=500, root=r"Dupe test"):
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 8)

        for folder in testfolders:
            arr = create_img_list(folder)
            if not arr:
                self.fail()

            result = find_dupes(arr, 4, threshold)
            if not result:
                self.fail()

            for a in result:
                self.assertEqual(len(a), 11)

    # Should not find any duplicates
    def test_dupes_false(self, threshold=500, root=r"dupe test 2"):
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        if not testfolders:
            self.fail()

        for folder in testfolders:
            arr = create_img_list(folder)
            if not arr:
                self.fail()

            result = find_dupes(arr, threshold)
            for a in result:
                self.assertEqual(len(a), None)

    # Test mixed folder of dupes and none dupes
    def test_dupe_mixed1c(self, threshold=200, root=r"dupe test 3/test 1"):

        # concurrent testing
        test1 = create_img_list(root)
        result1 = find_dupes(test1, 1, threshold)
        if self.assertEqual(len(result1), 2):
            for dupes in result1:
                for a in dupes:
                    a.display_path()
        else:
            for a in result1:
                self.assertEqual(len(a), 2)
                self.assertEqual(len(set(a)), 2)

    def test_dupe_mixed2c(self, threshold=200, root=r"Dupe test 3/Test 2"):

        test2 = create_img_list(root)
        result2 = find_dupes(test2, 1, threshold)
        if self.assertEqual(len(result2), 3):
            for dupes in result2:
                for a in dupes:
                    a.display_path()
        else:
            for a in result2:
                self.assertEqual(len(a), 2)
                self.assertEqual(len(set(a)), 2)

    def test_dupe_mixed1p(self, threshold=200, root=r"dupe test 3/Test 1"):
        # parallel testing
        test1 = create_img_list(root)
        result1 = find_dupes(test1, 2, threshold)
        if self.assertEqual(len(result1), 2):
            for dupes in result1:
                for a in dupes:
                    a.display_path()
        else:
            for a in result1:
                self.assertEqual(len(a), 2)
                self.assertEqual(len(set(a)), 2)

    def test_dupe_mixed2p(self, threshold=200, root=r"dupe test 3/Test 2"):

        test2 = create_img_list(root)
        result2 = find_dupes(test2, 2, threshold)
        if self.assertEqual(len(result2), 3):
            for dupes in result2:
                for a in dupes:
                    a.display_path()
        else:
            for a in result2:
                self.assertEqual(len(a), 2)
                self.assertEqual(len(set(a)), 2)


class TestApplication(TestCase):
    def setUp(self):
        # Set up the QApplication before running tests
        self.app = QApplication(sys.argv)

    def test_main_app(self):
        main_window = Application.MainWidget()
        main_window.initUI()

        self.assertIsInstance(main_window.file_menu, QMenu)
        options_action = main_window.file_menu.actions()[0]
        self.assertEqual(options_action.text(), "Options")

        options_action = main_window.action_menu.actions()[0]
        self.assertEqual(options_action.text(), "Clear Selected")
        self.assertIsInstance(main_window.image_list_widget, CheckListWidget)
        self.assertIsInstance(main_window.threshold_textbox, QLineEdit)
        self.assertIsInstance(main_window.dir_line1, QLineEdit)

    def test_threshold_textbox(self):
        # Create an instance of the main window class
        main_window = Application.MainWidget()
        # Call the method that creates the UI elements
        main_window.initUI()

        # Get the threshold_textbox widget
        threshold_textbox = main_window.threshold_textbox
        self.assertEqual(threshold_textbox.text(), "200")
        QTest.keyClick(threshold_textbox, Qt.Key_Backspace)
        self.assertEqual(threshold_textbox.text(), "20")
        QTest.keyClick(threshold_textbox, Qt.Key_0)
        QTest.keyClicks(threshold_textbox, "200")

    def tearDown(self):
        # Clean up the QApplication after running tests
        self.app.quit()


if __name__ == '__main__':
    TestCreate()
    TestSearch()
    TestApplication()