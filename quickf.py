# General purpose string and file handling library i grab functions from my programs to use

import pickle


def pickle_filename_dump(o, filename):
    if not filename.count('.'):
        filename += ".pkl"
    pickle.dump(o, file=open(filename, 'wb'))


def pickle_filename_load(filename):
    if not filename.count('.'):
        filename += ".pkl"
    return pickle.load(file=open(filename, 'rb'))


def tsv_to_arr(tsv):
    return [line.split('\t') for line in tsv.split('\n')]


def tsv_file_to_arr(f):
    return tsv_to_arr(f.read())


def replaceFromDict(s: str, dic: dict):
    for key, val in zip(dic.keys(), dic.values()):
        s = s.replace(key, val)
    return s


def file_lines(f):
    return f.read().split('\n')


def filename_lines(filename: str):
    return file_lines(open(filename, 'r', encoding="utf-8"))


def list_flatten(lst):
    out = []
    if type(lst) == (list or tuple):
        for a in lst:
            out += list_flatten(a)
        return out
    else:
        return [lst]


def str_pad(s: str, i: int):
    return s + " " * i


def list_pad(arr: list):
    arr = [str(a) for a in arr]
    padtarget = max(len(a) for a in arr)
    return [str_pad(a, padtarget - len(a)) for a in arr]


def database_pad(arr: list):
    out = [[] for _ in arr]
    for i in range(len(arr[0])):
        column = [a[i] for a in arr]
        column = list_pad(column)
        [out[x].append(val) for x, val in enumerate(column)]
    return out


def index_on(lst: list, func):  # Slow, not reccomended for intensive use
    index = [a for a in lst if func(a)]
    if len(index) == 0:
        return None
    return lst.index(index[0])


if __name__ == '__main__':
    b = [["passion", "name"],
         ["gastronomy", "jill"],
         ["stargasing", "bob"]]

    b = database_pad(b)

    print("\n".join("   ".join(a) for a in b))
