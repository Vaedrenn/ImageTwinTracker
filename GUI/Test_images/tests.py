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
    def test_dupes_false(self, threshold=500, root=r"Dupe test 2"):
        testfolders = root
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
    def test_dupe_mixed1c(self, threshold=200, root=r"Dupe test 3/test 1"):

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
        self.assertEqual(threshold_textbox.text(), "200")

        main_window.dir_line1.setText("Dupe test")
        self.assertEqual(main_window.dir_line1.text(), "Dupe test")

    def test__dupe_test1(self):
        main_window = Application.MainWidget()
        main_window.initUI()

        main_window.dir_line1.setText("Dupe test")
        self.assertEqual(main_window.dir_line1.text(), "Dupe test")

        self.assertEqual(main_window.image_list_widget.count(), 0)
        QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

        # Check if image_list_widget is updated
        final_item_count = main_window.image_list_widget.count()
        self.assertGreater(final_item_count, 0)

        self.assertEqual(final_item_count, len(main_window.images))

        # Check if images lines up
        for x in range(final_item_count):
            img = main_window.images[x]
            list_item = main_window.image_list_widget.item(x).text()
            self.assertEqual(img, list_item)
            if x > 0:
                self.assertFalse(img == main_window.images[x - 1])
                self.assertFalse(list_item == main_window.image_list_widget.item(x - 1).text())

        self.assertEqual(main_window.images.count(''), 9)

    def test__dupe_test2(self):
        main_window = Application.MainWidget()
        main_window.initUI()

        main_window.dir_line1.setText("Dupe test 2")
        self.assertEqual(main_window.dir_line1.text(), "Dupe test 2")

        self.assertEqual(main_window.image_list_widget.count(), 0)
        QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

        # Should be empty
        self.assertEqual(len(main_window.images), 0)
        self.assertEqual(main_window.image_list_widget.count(), 0)

    def test__dupe_test3(self):
        main_window = Application.MainWidget()
        main_window.initUI()

        main_window.dir_line1.setText("Dupe test 3/Test 1")
        self.assertEqual(main_window.dir_line1.text(), "Dupe test 3/Test 1")

        self.assertEqual(main_window.image_list_widget.count(), 0)
        QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

        # Check if image_list_widget is updated
        final_item_count = main_window.image_list_widget.count()
        self.assertGreater(final_item_count, 0)

        self.assertEqual(final_item_count, len(main_window.images))
        # Check if images lines up with

        for x in range(final_item_count):
            img = main_window.images[x]
            list_item = main_window.image_list_widget.item(x).text()
            self.assertEqual(img, list_item)
            if x > 0:
                self.assertFalse(img == main_window.images[x - 1])
                self.assertFalse(list_item == main_window.image_list_widget.item(x - 1).text())
            # spacer check
            if (x+1) % 3 == 0 and x != 0:
                self.assertEqual(img, '')
                self.assertEqual(list_item, '')
        self.assertEqual(main_window.images.count(''), 2)

        main_window.dir_line1.setText("Dupe test 3/Test 2")
        self.assertEqual(main_window.dir_line1.text(), "Dupe test 3/Test 2")

        self.assertEqual(main_window.image_list_widget.count(), 6)
        QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

        # Check if image_list_widget is updated
        final_item_count = main_window.image_list_widget.count()
        self.assertGreater(final_item_count, 0)

        self.assertEqual(final_item_count, len(main_window.images))
        # Check if images lines up with

        for x in range(final_item_count):
            img = main_window.images[x]
            list_item = main_window.image_list_widget.item(x).text()
            self.assertEqual(img, list_item)
            if x > 0:
                self.assertFalse(img == main_window.images[x - 1])
                self.assertFalse(list_item == main_window.image_list_widget.item(x - 1).text())
            # spacer check
            if (x+1) % 3 == 0 and x != 0:
                self.assertEqual(img, '')
                self.assertEqual(list_item, '')
        self.assertEqual(main_window.images.count(''), 3)

    def test__valid_test(self):
        def test__dupe_test3(self):
            main_window = Application.MainWidget()
            main_window.initUI()

            main_window.dir_line1.setText("Tensor test")
            self.assertEqual(main_window.dir_line1.text(), "Tensor test")

            self.assertEqual(main_window.image_list_widget.count(), 0)
            QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

            # Check if image_list_widget is updated
            final_item_count = main_window.image_list_widget.count()
            self.assertGreater(final_item_count, 0)

            self.assertEqual(final_item_count, len(main_window.images))
            # Check if images lines up with

            for x in range(final_item_count):
                img = main_window.images[x]
                list_item = main_window.image_list_widget.item(x).text()
                self.assertEqual(img, list_item)
                if x > 0:
                    self.assertFalse(img == main_window.images[x - 1])
                    self.assertFalse(list_item == main_window.image_list_widget.item(x - 1).text())
            # spacer check
            self.assertEqual(main_window.images.count(''), 1)
            self.assertEqual(len(main_window.images), 11)
            # check for dud
            self.assertEqual(main_window.images.count('dud.txt'), 0)


    def tearDown(self):
        # Clean up the QApplication after running tests
        self.app.quit()


if __name__ == '__main__':
    TestCreate()
    TestSearch()
    TestApplication()
