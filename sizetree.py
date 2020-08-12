import os.path
import json
from quickf import list_flatten


class FilenameHolder:
    def __init__(self, root=None):
        self.root = root
        # print("Walking")
        self.walk = str_walk_to_dict(root)
        # print("Parsing")
        self.classes = self._parse_classes(root)
        # print(self.classes)

        # for path, (dicts, files) in self.walk.items():

    def _parse_classes(self, path):
        out = []

        # print(self.walk[path])
        print(path)
        childpaths = [self._parse_classes(path + '\\' + dct) for dct in self.walk[path][0]]
        childpaths = list_flatten(childpaths)
        childpaths += [File(self, path + '\\' + file) for file in self.walk[path][1]]
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


class File(Path):
    def __init__(self, parent: FilenameHolder, path: str):
        super().__init__(parent, path)
        assert os.path.isfile(path), path

    def get_size(self):
        if self.size is None:
            self.size = os.path.getsize(
                self.absolute_path)  # TODO move to init
        return self.size

    def get_info_dict(self):
        return {"t": self.__class__.__name__, "n": self.name, "s": self.get_size(), }
        # Type, name, size


class Directory(Path):
    def __init__(self, path: str, content_indexes: list, parent: FilenameHolder):
        super().__init__(parent, path)
        self.contents = content_indexes
        assert os.path.isdir(path)

    def get_size(self):
        if self.size is None:
            self.size = sum(ptr.get_size() for ptr in self.contents)
        return self.size

    def get_info_dict(self):
        return {"t": self.__class__.__name__, "n": self.name, "s": self.get_size(),
                "c": [a.get_info_dict() for a in self.contents]}
    # Type, name, size, contents


def walk_to_dict(walk: list):
    out = {}
    for path, dirs, files in walk:
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
    rootdir = ".."

    walk = FilenameHolder(rootdir)
    paths = walk.classes

    with open("sizes.json", "w") as f:
        f.write("var data = ")
        json.dump(walk.classes[-1].get_info_dict(), f, indent=4)
    # json.loads(str(paths[0], )

    # for path, dirs, files in size_format_walk(rootdir):
    #    print(path, dirs, files)
