import os
import re


class DirHandler:
    """
    Used to recursively iterate files inside dirs
    """
    def __init__(self, dir_path, mask='.*', max_level=None):
        """
        :param dir_path: root path (from where to search)
        :param mask: which files are acceptable. Also affect which dirs will be used to recursive run
        :param max_level: max recursion level
        """
        self._dir_path = dir_path
        self._list = [os.path.join(self._dir_path, x) for x in os.listdir(dir_path) if re.match(mask, x)]
        self._pos = -1
        self._mask = mask
        self._inner_level = None
        self._max_level = max_level

    def __iter__(self):
        if self._max_level == 0:
            return iter(self._list)
        else:
            return self

    def __next__(self):
        return self.__move(DirHandler._next_file)

    next = __next__

    def prev(self):
        """ to achieve last element (first in backward iteration) used _file first """
        return self.__move(DirHandler._prev_file)

    def __move(self, direction_func):
        """ move (forward or backward) """
        if self._inner_level is not None:
            try:
                return self._inner_level.__move(direction_func)
            except StopIteration:  # inner level exhausted
                self._inner_level = None
                return self.__move_on_top_level(direction_func)
        else:
            return self.__move_on_top_level(direction_func)

    def __move_on_top_level(self, direction_func):
        file = direction_func(self)
        if os.path.isfile(file):
            return file
        else:
            self._inner_level = self._create_inner(file, self.__inner_max_level())
            return self.__move(direction_func)

    def _create_inner(self, file, level):
        return DirHandler(file, self._mask, level)

    def _next_file(self):
        self._pos += 1
        if self._pos < len(self._list):
            return self._file()
        else:
            raise StopIteration

    def _prev_file(self):
        # allow first move backward looping but disallow other; hack
        if self._pos == -1:
            self._pos = len(self._list) - 1
            return self._file()
        elif self._pos >= 0:
            self._pos -= 1
            if self._pos == -1:
                self._pos = -2  # block from future backward move
            return self._file()
        else:
            raise StopIteration

    def _file(self):
        """ by default DirHandler point to last item. If you want forward iterate use next """
        return self._list[self._pos]

    def __to_end(self):
        self._pos = len(self._list)

    def __inner_max_level(self):
        if self._max_level is None:
            return None
        else:
            return self._max_level - 1
