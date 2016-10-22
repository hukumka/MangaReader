import pickle
import os
from PyQt5.QtWidgets import QFileDialog

from MangaContentsModel import MangaContentsModel, get_full_position
from GlobalData import global_data


#   Save load for MangaContentsModel model

#  it's friend to MangaContentsModel
def save_manga_state(model, file_path=None):
    root = model.invisibleRootItem()
    if file_path is None:
        file_path = manga_pickle_by_path(root._path)

    data = {
        'position': get_full_position(root),
        'path': root._path
    }

    with open(file_path, 'wb') as f:
        pickle.dump(data, f)


def load_manga_state(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    model = MangaContentsModel(data['path'])
    set_manga_model_pos(model, data['position'])
    return model


def load_manga_folder(path):
    if os.path.isfile(path):
        return load_manga_state(path)
    elif os.path.isdir(path):
        pickle_path = manga_pickle_by_path(path)
        if os.path.exists(pickle_path):
            return load_manga_state(pickle_path)
        else:
            return MangaContentsModel(path)


def set_manga_model_pos(model, pos):
    node = model.invisibleRootItem()
    for x in pos:
        node._pos = x
        node = node.inner()


def get_default_manga():
    path = global_data.get('current_manga')
    if path is None:
        return None
    else:
        return load_manga_folder(path)


def manga_pickle_by_path(path):
    return os.path.join(path, 'data.pickle')


def manga_selection_dialog(default_path, parent=None):
    manga_path = QFileDialog.getExistingDirectory(
        parent, caption="open manga folder",
        directory=default_path,
        options=QFileDialog.ShowDirsOnly
    )
    if not manga_path:
        return None
    else:
        global_data.set('current_manga', manga_path)
        return load_manga_folder(manga_path)
