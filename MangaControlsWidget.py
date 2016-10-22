import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTreeView
from PyQt5.QtCore import QItemSelectionModel, Qt

from EasyScaleView import EasyScaleView
from MangaSelection import get_default_manga, manga_selection_dialog, save_manga_state
from GlobalData import global_data


class Display(EasyScaleView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentScale = global_data.get('zoom')

    def zoom(self, mul):
        super().zoom(mul)
        global_data.set('zoom', self.currentScale)


class MangaControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        self.__init_done = False

        self.__model = None
        model = get_default_manga()
        if model is None:
            model = manga_selection_dialog('~', self)

        self.__contents = QTreeView()
        self.__contents.setMaximumWidth(200)
        self.__contents.setMinimumWidth(150)
        if not global_data.get('show_contents'):
            self.__contents.hide()
        self.__display = Display()
        self.__contents.setFocusProxy(self.__display)
        self.layout().addWidget(self.__contents)
        self.layout().addWidget(self.__display)
        self.set_model(model)

    def set_model(self, model):
        self.__model = model
        self.__contents.setModel(model)

        self.__model.position_changed.connect(self.on_position_change)
        self.__contents.selectionModel().currentChanged.connect(self.selection_changed)
        self.sync_selection()
        self.__display.display_image(self.__model.current())

    def selection_changed(self, index):
        if self.__init_done:
            self.__model.select(index)
        else:
            self.__init_done = True

    def on_position_change(self, path):
        self.__display.display_image(path)
        self.sync_selection()
        save_manga_state(self.__model)

    def sync_selection(self):
        index = self.__model._current_index()
        self.__contents.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectCurrent)

    def open_dialog(self):
        path, _ = os.path.split(self.__model.path())
        model = manga_selection_dialog(path, self)
        if model is not None:
            self.set_model(model)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C:
            self.toggle_contents()
        elif event.key() == Qt.Key_Plus:
            self.__display.zoom(1.05)
        elif event.key() == Qt.Key_Minus:
            self.__display.zoom(1/1.05)
        elif event.key() == Qt.Key_J:
            self.__display.scroll(100)
        elif event.key() == Qt.Key_K:
            self.__display.scroll(-100)
        elif event.key() == Qt.Key_L:
            self.__model.next()
        elif event.key() == Qt.Key_H:
            self.__model.prev()
        else:
            event.ignore()

    def toggle_contents(self):
        showed = global_data.get('show_contents')
        if showed:
            self.__contents.hide()
        else:
            self.__contents.show()
        global_data.set('show_contents', not showed)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QTreeView, QApplication
    import sys
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    #  example
    app = QApplication(sys.argv)
    w = MangaControlsWidget()
    w.show()
    sys.exit(app.exec())
