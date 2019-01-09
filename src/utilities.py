from time import localtime
import os


def accumulate_vector(vector):
    anl = [vector[0]]
    if len(vector) >= 2:
        for index in range(1, len(vector)):
            anl.append(anl[index - 1] + vector[index])
    return anl


def normalize_vector(vector):
    total = 0
    for entry in vector:
        total += entry
    return [entry / total for entry in vector] if total != 0 else 1 / len(vector)


def get_date_in_string():
    date = localtime()
    return str(date.tm_year) + '_' + str(date.tm_mon) + '_' + \
           str(date.tm_mday) + '_' + str(date.tm_hour) + '_' + \
           str(date.tm_min) + '_' + str(date.tm_sec)


def decode_stdout(stdout):
    stdout = stdout.decode('ascii')
    index, fitness = [x for x in stdout.split(',')]
    return index, fitness


def remove_tmp(path):
    if os.path.exists(path):
        os.remove(path)