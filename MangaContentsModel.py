import os
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSignal


def clone_method(obj, cls, method_name):
    method = getattr(cls, method_name)
    setattr(obj, method_name, lambda *args, **kwargs: method(obj, *args, **kwargs))


def get_full_position(root):
    node = root
    pos = []
    while node._is_dir: # @suppress_warning
        pos.append(node._pos)
        node = node.child(pos[-1])
    return pos


class MangaContentsItem(QStandardItem):
    def __init__(self, path, is_dir=True):
        super().__init__()
        self._pos = 0
        self._is_dir = is_dir
        self._path = path
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    @staticmethod
    def set_interface(item, path, is_dir=True):
        """ it is so stupid but works """
        item._pos = 0
        item._is_dir = is_dir
        item._path = path
        for method in ['inner', 'next', 'prev', 'current', 'to_end', 'to_begin', 'top_level_node', 'child_count', 'find_position']:
            clone_method(item, MangaContentsItem, method)

    def data(self, role):
        if role == Qt.DisplayRole:
            return os.path.basename(self._path)
        else:
            return None

    def find_position(self, item):
        for i in range(self.child_count()):
            if item is self.child(i):
                return i
        return None

    def next(self):
        if self._is_dir:
            try:
                self.inner().next()
            except StopIteration:
                self._pos += 1
                if self._pos == self.child_count():
                    raise StopIteration()
                self.inner()._pos = 0
        else:
            raise StopIteration()
        return self.current()

    def prev(self):
        if self._is_dir:
            try:
                self.inner().prev()
            except StopIteration:
                self._pos -= 1
                if self._pos == -1:
                    raise StopIteration()
                self.inner()._pos = self.inner().child_count() - 1
        else:
            raise StopIteration()
        return self.current()

    def current(self):
        if self._is_dir:
            return self.inner().current()
        else:
            return self._path

    def child_count(self):
        return self.rowCount()

    def to_end(self):
        if self._is_dir:
            self._pos = self.child_count() - 1
            self.inner().to_end()

    def to_begin(self):
        if self._is_dir:
            self._pos = 0
            self.inner().to_begin()

    def inner(self):
        if self._is_dir:
            return self.child(self._pos)
        else:
            return self

    def top_level_node(self):
        if self._is_dir:
            return self.inner().top_level_node()
        else:
            return self


class MangaContentsModel(QStandardItemModel):
    position_changed = pyqtSignal(str)

    def __init__(self, path):
        super().__init__()
        MangaContentsItem.set_interface(self.invisibleRootItem(), path)
        self.__root = self.invisibleRootItem()
        self.load(path, self.invisibleRootItem())

    def path(self):
        return self.__root._path

    def load(self, path, root):
        if os.path.isdir(path):
            for e in os.scandir(path):
                if e.is_dir() or os.path.splitext(e.path)[1] != '.pickle':
                    child = MangaContentsItem(e.path, e.is_dir())
                    self.load(e.path, child)
                    root.appendRow(child)

    def select(self, index):
        old_pos = get_full_position(self.invisibleRootItem())
        self.__select_from_item(self.itemFromIndex(index))
        new_pos = get_full_position(self.invisibleRootItem())
        if new_pos != old_pos:
            self.__emit_position_changed()

    def __select_from_item(self, item, pos=0):
        item._pos = pos
        if item.parent():
            self.__select_from_item(item.parent(), item.parent().find_position(item))
        else:
            self.invisibleRootItem()._pos = self.invisibleRootItem().find_position(item)

    def flags(self, index):
        if not index.isValid():
            return 0
        else:
            return super().flags(index)

    def next(self):
        path = self.__root.next()
        self.__emit_position_changed()
        return path

    def __emit_position_changed(self):
        self.position_changed.emit(self.invisibleRootItem().current())

    def prev(self):
        path = self.__root.prev()
        self.__emit_position_changed()
        return path

    def current(self):
        return self.__root.current()

    def next_chapter(self):
        self.__root.inner().to_end()
        return self.next()

    def prev_chapter(self):
        self.__root.inner().to_begin()
        return self.prev()

    def _current_index(self):
        node = self.__root.top_level_node()
        return node.index()


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
    model = MangaContentsModel("D:/manga/dorohedoro")
    model.next_chapter()
    model.next_chapter()
    model.next()

    w = QTreeView()
    w.setModel(model)
    w.show()
    sys.exit(app.exec())
