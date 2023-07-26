from PyQt5.QtGui import QPalette, QColor


def create_light_palette():
    light_palette = QPalette()
    light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.WindowText, QColor(40, 40, 40))
    light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))
    light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
    light_palette.setColor(QPalette.ToolTipText, QColor(40, 40, 40))
    light_palette.setColor(QPalette.Text, QColor(40, 40, 40))
    light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ButtonText, QColor(40, 40, 40))
    light_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    light_palette.setColor(QPalette.Link, QColor(0, 153, 255))
    light_palette.setColor(QPalette.Highlight, QColor(0, 153, 255))
    light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    return light_palette
