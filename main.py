from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout

from MangaControlsWidget import MangaControlsWidget as Viewer
from GlobalData import global_data


class HelpWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QFormLayout())
        self.layout().addRow("hjkl",  QLabel("Vim style navigation"))
        self.layout().addRow("c(ontents)",  QLabel("toggle contents panel"))
        self.layout().addRow("F1",  QLabel("toggle help panel (this)"))
        self.layout().addRow("q(uit)",  QLabel("Exit from manga viewer"))
        self.layout().addRow("o(pen)",  QLabel("Open manga folder"))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.__help = HelpWidget()
        self.__viewer = Viewer()
        self.layout().addWidget(self.__help)
        self.layout().addWidget(self.__viewer)
        if not global_data.get('show_help'):
            self.__help.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()
        elif event.key() == Qt.Key_F1:
            self.__toggle_help()
        elif event.key() == Qt.Key_O:
            self.__viewer.open_dialog()
        else:
            pass

    def __toggle_help(self):
        showed = global_data.get('show_help')
        if showed:
            self.__help.hide()
        else:
            self.__help.show()
        global_data.set('show_help', not showed)


if __name__ == '__main__':
    import sys
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    view = Window()
    view.showFullScreen()
    sys.exit(app.exec())

