import sys
from unittest import TestCase

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QLineEdit

from GUI import Application
from GUI.CheckListWidget import CheckListWidget


class TestApplication(TestCase):
    def setUp(self):
        # Set up the QApplication before running tests
        self.app = QApplication(sys.argv)

    # bare minimum checking
    def test_main_app(self):
        main_window = Application.MainWidget()
        main_window.initUI()

        self.assertIsInstance(main_window.image_list_widget, CheckListWidget)
        self.assertIsInstance(main_window.threshold_textbox, QLineEdit)
        self.assertIsInstance(main_window.dir_line1, QLineEdit)

    # Test if keys work
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

    # find dupes action testing, check if it locates dupes
    def test__dupe_test1(self):
        main_window = Application.MainWidget()
        main_window.initUI()
        # check dirs
        main_window.dir_line1.setText("Dupe test")
        self.assertEqual(main_window.dir_line1.text(), "Dupe test")
        # check initial count and then click
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
        # Spacers check
        self.assertEqual(main_window.images.count(''), 9)

    # No dupes here
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

    # Test mixed folders of dupes and non dupes
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

        # Check if images lines
        for x in range(final_item_count):
            img = main_window.images[x]
            list_item = main_window.image_list_widget.item(x).text()
            self.assertEqual(img, list_item)
            if x > 0:
                self.assertFalse(img == main_window.images[x - 1])
                self.assertFalse(list_item == main_window.image_list_widget.item(x - 1).text())
            # spacer check
            if (x + 1) % 3 == 0 and x != 0:
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

        # Check if images lines up
        for x in range(final_item_count):
            img = main_window.images[x]
            list_item = main_window.image_list_widget.item(x).text()
            self.assertEqual(img, list_item)
            if x > 0:
                self.assertFalse(img == main_window.images[x - 1])
                self.assertFalse(list_item == main_window.image_list_widget.item(x - 1).text())
            # spacer check
            if (x + 1) % 3 == 0 and x != 0:
                self.assertEqual(img, '')
                self.assertEqual(list_item, '')
        self.assertEqual(main_window.images.count(''), 3)

    # Check if invalid files are added
    def test__valid_test(self):

        main_window = Application.MainWidget()
        main_window.initUI()

        main_window.dir_line1.setText("Tensor test")
        self.assertEqual(main_window.dir_line1.text(), "Tensor test")

        self.assertEqual(main_window.image_list_widget.count(), 0)
        QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

        # Check if image_list_widget is updated
        final_item_count = main_window.image_list_widget.count()
        self.assertEqual(final_item_count, 12)
        self.assertEqual(final_item_count, len(main_window.images))

        # Check if images lines up
        for x in range(final_item_count):
            img = main_window.images[x]
            list_item = main_window.image_list_widget.item(x).text()
            self.assertEqual(img, list_item)
            if x > 0:
                self.assertFalse(img == main_window.images[x - 1])
                self.assertFalse(list_item == main_window.image_list_widget.item(x - 1).text())

        # spacer check
        self.assertEqual(main_window.images.count(''), 1)
        self.assertEqual(len(main_window.images), 12)  # 11 dupes and 1 spacer
        # check for dud
        self.assertEqual(main_window.images.count('dud.txt'), 0)

    def tearDown(self):
        # Clean up the QApplication after running tests
        self.app.quit()


if __name__ == '__main__':
    TestApplication()
