from time import localtime
from os import walk
import os


def clean_dir(dir):
    for (dirpath, dirnames, filenames) in walk(dir):
        for name in filenames:
            path = dir + '/' + name
            remove_file(path)


def average_tuple(t):
    total = 0
    for elem in t:
        total += elem
    return total / len(t)


def accumulate_tuple(t):
    anl = [t[0]]
    if len(t) >= 2:
        for index in range(1, len(t)):
            anl.append(anl[index - 1] + t[index])
    return anl


def normalize_tuple(t):
    total = 0
    for elem in t:
        total += elem
    return [elem / total for elem in t] if total != 0 else [1 / len(t) for _ in range(len(t))]


def get_date_in_string():
    date = localtime()
    return str(date.tm_year) + '_' + str(date.tm_mon) + '_' + \
           str(date.tm_mday) + '_' + str(date.tm_hour) + '_' + \
           str(date.tm_min) + '_' + str(date.tm_sec)


def decode_stdout(stdout):
    stdout = stdout.decode('ascii')
    index, fitness = [x for x in stdout.split(',')]
    return index, fitness


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
