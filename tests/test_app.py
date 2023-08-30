import os
import sys

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QLineEdit

from ImageTwinTracker.gui import Application
from ImageTwinTracker.gui.CheckListWidget import CheckListWidget


@pytest.fixture
def app_qt():
    # Set up the QApplication before running tests
    app = QApplication(sys.argv)
    yield app
    # Tear down the QApplication after the test is done
    app.quit()

@pytest.fixture
def main_window():
    return Application.MainWidget()


# test if the important bits are there
def test_main_app(app_qt, main_window):
    assert isinstance(main_window.image_list_widget, CheckListWidget)
    assert isinstance(main_window.threshold_textbox, QLineEdit)
    assert isinstance(main_window.dir_line1, QLineEdit)


# Test if keys work
def test_threshold_textbox(app_qt, main_window):
    threshold_textbox = main_window.threshold_textbox
    assert threshold_textbox.text() == "200"

    QTest.keyClick(threshold_textbox, Qt.Key_Backspace)
    assert threshold_textbox.text() == "20"

    QTest.keyClick(threshold_textbox, Qt.Key_0)
    assert threshold_textbox.text() == "200"

    main_window.dir_line1.setText("Dupe test")
    assert main_window.dir_line1.text() == "Dupe test"


# find dupes action testing, check if it locates dupes

def test_dupe_test1(app_qt, main_window):
    # check dirs
    main_window.dir_line1.setText("tests/Dupe test")
    assert main_window.dir_line1.text() == "tests/Dupe test"

    # check initial count and then click
    assert main_window.image_list_widget.count() == 0
    QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

    # Check if image_list_widget is updated
    final_item_count = main_window.image_list_widget.count()
    assert final_item_count > 0
    assert final_item_count == len(main_window.images)

    # Check if images lines up
    for x in range(final_item_count):
        img = main_window.images[x]
        list_item = main_window.image_list_widget.item(x).text()
        assert img == list_item
        if x > 0:
            assert img != main_window.images[x - 1]
            assert list_item != main_window.image_list_widget.item(x - 1).text()
    # Spacers check
    assert main_window.images.count('') == 7


# No dupes here
def test_dupe_test2(app_qt, main_window):
    main_window.dir_line1.setText("tests/Dupe test 2")
    assert main_window.dir_line1.text() == "tests/Dupe test 2"

    assert main_window.image_list_widget.count() == 0
    QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

    assert len(main_window.images) == 0
    assert main_window.image_list_widget.count() == 0


# Test mixed folders of dupes and non dupes
def test_dupe_test3(app_qt, main_window):
    main_window.dir_line1.setText("tests/Dupe test 3/Test 1")
    assert main_window.dir_line1.text() == "tests/Dupe test 3/Test 1"

    assert main_window.image_list_widget.count() == 0
    QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

    final_item_count = main_window.image_list_widget.count()
    assert final_item_count > 0
    assert final_item_count == len(main_window.images)

    for x in range(final_item_count):
        img = main_window.images[x]
        list_item = main_window.image_list_widget.item(x).text()
        assert img == list_item
        if x > 0:
            assert img != main_window.images[x - 1]
            assert list_item != main_window.image_list_widget.item(x - 1).text()

        if (x + 1) % 3 == 0 and x != 0:
            assert img == ''
            assert list_item == ''
    assert main_window.images.count('') == 1

    main_window.dir_line1.setText("tests/Dupe test 3/Test 2")
    assert main_window.dir_line1.text() == "tests/Dupe test 3/Test 2"

    assert main_window.image_list_widget.count() == 5
    QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

    final_item_count = main_window.image_list_widget.count()
    assert final_item_count > 0
    assert final_item_count == len(main_window.images)

    for x in range(final_item_count):
        img = main_window.images[x]
        list_item = main_window.image_list_widget.item(x).text()
        assert img == list_item
        if x > 0:
            assert img != main_window.images[x - 1]
            assert list_item != main_window.image_list_widget.item(x - 1).text()

        if (x + 1) % 3 == 0 and x != 0:
            assert img == ''
            assert list_item == ''
    assert main_window.images.count('') == 2


def test_valid_test(app_qt, main_window):
    main_window.dir_line1.setText("tests/Tensor test")
    assert main_window.dir_line1.text() == "tests/Tensor test"

    assert main_window.image_list_widget.count() == 0
    QTest.mouseClick(main_window.threshold_button, Qt.LeftButton)

    final_item_count = main_window.image_list_widget.count()
    assert final_item_count == 11
    assert final_item_count == len(main_window.images)

    for x in range(final_item_count):
        img = main_window.images[x]
        list_item = main_window.image_list_widget.item(x).text()
        assert img == list_item
        if x > 0:
            assert img != main_window.images[x - 1]
            assert list_item != main_window.image_list_widget.item(x - 1).text()

    assert main_window.images.count('') == 0
    assert len(main_window.images) == 11
    assert main_window.images.count('dud.txt') == 0