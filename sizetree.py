import os.path
import json
from quickf import list_flatten


class FilenameHolder:
    def __init__(self, root, print_stages=False, print_indexed_dirs=True):
        self.root = root
        if self.root[-1] == '\\':
            self.root = root[:-1]

        self.new_uid = 0

        if print_stages:
            print("Walking")
        self.walk = str_walk_to_dict(root)

        if print_stages:
            print("Parsing")
        self.print_indexed = print_indexed_dirs
        self.classes = self._parse_classes(self.root)

        # print(self.classes)

        # for path, (dicts, files) in self.walk.items():

    def _parse_classes(self, path):
        out = []

        # print(self.walk[path])
        try:
            walkpath = self.walk[path]
        except KeyError:
            return

        if self.print_indexed:
            print(path)

        childpaths = [self._parse_classes(path + '\\' + dct) for dct in walkpath[0]]
        childpaths = list_flatten(childpaths)
        childpaths += [File(self, path + '\\' + file) for file in walkpath[1]]
        out.append(Directory(path, childpaths, self))

        return out

    def __call__(self, *args, **kwargs):
        return self.walk, self.classes


class Path:
    def __init__(self, parent: FilenameHolder, path: str = None):
        self.name = path.split('\\')[-1]
        self.absolute_path = path
        self.size = None
        self.parent = parent
        self.uid = parent.new_uid
        parent.new_uid += 1


class File(Path):
    def __init__(self, parent: FilenameHolder, path: str):
        super().__init__(parent, path)
        # assert os.path.isfile(path), path
        # Commenting this ^ code out is probably a bad idea but if the file is open it raises the error incorrectly
        # replaced this with this code
        if not os.path.isfile(path):
            del self

    def get_size(self):
        if self.size is None:
            try:
                self.size = os.path.getsize(
                    self.absolute_path)  # TODO move to init
            except FileNotFoundError:  # Incase the file was deleted while the program was running
                del self
                return 0
            except OSError:
                del self
                return 0
        return self.size

    def get_info_dict(self):
        return {"i": self.uid, "t": self.__class__.__name__[0], "n": self.name, "s": self.get_size(), }
        # id, Type, name, size


class Directory(Path):
    def __init__(self, path: str, content_indexes: list, parent: FilenameHolder):
        super().__init__(parent, path)
        self.contents = [index for index in content_indexes if index is not None]  # Protects against some wierd bug
        assert os.path.isdir(path)

    def get_size(self):
        if self.size is None:
            self.size = sum(ptr.get_size() for ptr in self.contents)
        return self.size

    def get_info_dict(self):
        return {"i": self.uid, "t": self.__class__.__name__[0], "n": self.name, "s": self.get_size(),
                "c": [a.get_info_dict() for a in self.contents]}
    # id, Type, name, size, contents


def walk_to_dict(walk: list):
    out = {}
    for path, dirs, files in walk:
        if path[-1] == '\\':
            path = path[:-1]
        out[path] = (dirs, files)
    return out


def str_walk_to_dict(root: str):
    return walk_to_dict(list(os.walk(root, False)))


def index_on(lst: list, func):
    index = [a for a in lst if func(a)]
    if len(index) == 0:
        return None
    return lst.index(index[0])


if __name__ == '__main__':
    input("you have run the WRONG FILE, run gui.py instead")


