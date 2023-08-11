import sys

from PyQt5.QtWidgets import QApplication

from Application import MainWidget


def main():
    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()