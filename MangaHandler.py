from dir_iter import DirHandler

import pickle
import os


class MangaHandler(DirHandler):
    """ used to iterate leaf over pages and volumes """
    def __init__(self, path, mask=r"(?!.*\.pickle)", max_level=None):
        super().__init__(path, mask, max_level)

    def next_chapter(self):
        self.__skip_on_level()
        return next(self)

    def dir(self):
        return self._dir_path

    def prev_chapter(self):
        self.__skip_on_level()
        return self.prev()

    def __skip_on_level(self, level=0):
        if level == 0:
            self._inner_level = None
        elif self._inner_level is not None:
            self._inner_level.move_on_level(level - 1)

    def current(self):
        if self._inner_level is None:
            return self._file()
        else:
            return MangaHandler.current(self._inner_level)

    def save(self, path=None):
        pos = list(self.__yield_pos())
        data = {
            "pos": pos,
            "mask": self._mask,
            "path": self._dir_path,
            "max": self._max_level
        }
        if path is not None:
            pickle.dump(data, open(path, 'wb'))
        path = self.__handler_path(self._dir_path)
        pickle.dump(data, open(path, 'wb'))

    @staticmethod
    def __handler_path(path):
        return os.path.join(path, 'handler.pickle')

    @staticmethod
    def load(manga_dir, handler_file=None):
        if handler_file is None:
            handler_file = MangaHandler.__handler_path(manga_dir)

        handler = MangaHandler.load_fail(handler_file)
        if handler is None:
            handler = MangaHandler(manga_dir)
            handler.next()
        return handler

    @staticmethod
    def load_fail(handler_file):
        try:
            data = pickle.load(open(handler_file, 'rb'))
            dir_iter = MangaHandler(data['path'], data['mask'], data['max'])
            dir_iter.__move_to_pos(iter(data['pos']))
            return dir_iter
        except FileNotFoundError:
            return None

    def __move_to_pos(self, pos_iter):
        try:
            self._pos = next(pos_iter)
            file = self._file()
            if os.path.isdir(file):
                self._inner_level = self._create_inner(self._file(), self._max_level)
                MangaHandler.__move_to_pos(self._inner_level, pos_iter)
        except StopIteration:
            pass

    def __yield_pos(self):
        yield self._pos
        if self._inner_level is not None:
            for p in MangaHandler.__yield_pos(self._inner_level):
                yield p