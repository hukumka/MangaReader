import os
import pickle


def auto_save(func):
    def a(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.save()
    return a


class GlobalData:
    data_path = os.path.join(os.path.expanduser('~'), '.manga_viewer_globals.pickle')
    default_globals = {
        'current_manga': None,
        'show_help': True,
        'show_contents': False,
        'zoom': 1.0
    }

    def __init__(self):
        if not self.__load():
            self.__init_default()

    def __load(self):
        if os.path.isfile(self.data_path):
            # loading
            with open(self.data_path, 'rb') as f:
                self.__data = pickle.load(f)

            # if recent app uses more values, init them
            for key, value in self.default_globals.items():
                if key not in self.__data:
                    self.__data[key] = value
            return True
        else:
            return False

    def __init_default(self):
        self.__data = self.default_globals

    def save(self):
        with open(self.data_path, 'wb') as f:
            pickle.dump(self.__data, f)

    def get(self, attr):
        return self.__data[attr]

    def set(self, attr, value):
        if attr in self.__data:
            self.__data[attr] = value
            self.save()
        else:
            raise KeyError()

global_data = GlobalData()
