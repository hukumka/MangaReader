from os import path as path

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QGraphicsPixmapItem

from EasyScaleView import EasyScaleView
from MangaHandler import MangaHandler


class Viewer(EasyScaleView):
    handler_path = path.join(path.expanduser('~'), '.manga_viewer.pickle')

    def __init__(self, parent=None):
        self.currentScale = 1.0
        self.__scene = QGraphicsScene(parent)
        EasyScaleView.__init__(self, self.__scene)
        self._handler = None

    def open_manga(self, manga_path):
        self.open_mange_from_handler(MangaHandler.load(manga_path))

    def open_mange_from_handler(self, handler):
        self._handler = handler
        self.display_image(self._handler.current())

    def prev(self):
        self.display_image(self._handler.prev())

    def next(self):
        self.display_image(self._handler.next())

    def save(self):
        self._handler.save(self.handler_path)

    def next_chapter(self):
        self.display_image(self._handler.next_chapter())

    def prev_chapter(self):
        self.display_image(self._handler.prev_chapter())

    def display_image(self, image_path):
        print(image_path)
        self.__scene.clear()
        item = QGraphicsPixmapItem(QPixmap(image_path))
        self.__scene.addItem(item)
        self.verticalScrollBar().setValue(0)
        self.update_scale()
        self.save()

    def scroll(self, offset):
        scroll = self.verticalScrollBar()
        scroll.setValue(scroll.value() + offset)


class ViewerAutoSaveLoad(Viewer):
    def __init__(self, parent=None):
        Viewer.__init__(self, parent)
        self._handler = self.load_last_manga()

    def load_last_manga(self):
        self._handler = MangaHandler.load_fail(self.handler_path)
        if self._handler is None:
            self.__open_dialog()
        else:
            self.display_image(self._handler.current())
        return self._handler

    def open_dialog(self):
        if self._handler is not None and self._handler.dir() != '':
            manga_dir = path.join(self._handler.dir(), path.pardir)
        else:
            manga_dir = 'C:/'
        manga_dir = QFileDialog.getExistingDirectory(
            self, caption="open manga folder",
            directory=manga_dir,
            options=QFileDialog.ShowDirsOnly
        )
        if manga_dir != '':
            self.open_manga(manga_dir)
