from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QStackedLayout, QLabel

from Viewer import ViewerAutoSaveLoad as Viewer


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QStackedLayout()
        self.layout.setStackingMode(QStackedLayout.StackAll)
        self.layout.setAlignment(Qt.AlignCenter)

        self.viewer = Viewer(self)
        self.layout.addWidget(self.viewer)

        help = QLabel("\n".join([
                      "hjkl - navigation",
                      "b(ack) - previous chapter",
                      "n(ext) - next chapter",
                      "o(pen) - open manga folder",
                      "q(uit) - quit reader",
                      "F1 - toggle help"]),
                      )
        help.setVisible(False)
        self.layout.addWidget(help)

        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()
        elif event.key() == Qt.Key_F1:
            self.layout.setCurrentIndex(1 - self.layout.currentIndex())
        elif event.key() == Qt.Key_O:
            self.viewer.open_dialog()
        elif event.key() == Qt.Key_L:
            self.viewer.next()
        elif event.key() == Qt.Key_H:
            self.viewer.prev()
        elif event.key() == Qt.Key_K:
            self.viewer.scroll(-100)
        elif event.key() == Qt.Key_J:
            self.viewer.scroll(100)
        elif event.key() == Qt.Key_N:
            self.viewer.next_chapter()
        elif event.key() == Qt.Key_B:
            self.viewer.prev_chapter()
        elif event.key() == Qt.Key_Plus:
            self.viewer.zoom(1.05)
        elif event.key() == Qt.Key_Minus:
            self.viewer.zoom(1/1.05)
        else:
            pass


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

