import os
from math import exp, pow, sqrt
from os import walk
from random import randint, random
from time import localtime


def std_tuple(t):
    if len(t) > 1:
        average = average_tuple(t)
        summed = 0
        for elem in t:
            summed += pow(elem - average, 2)
        return sqrt(summed/(len(t) - 1))
    else:
        return 0


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
    return float(stdout.decode('ascii'))


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def choose_random_element(arr):
    return arr[randint(0, len(arr) - 1)]


def poisson_random_number(lambda_):
    L = exp(-lambda_)
    poisson_number = 0
    p = 1
    while True:
        poisson_number += 1
        u = random()
        p = p * u
        if p < L:
            break
    return poisson_number - 1


if __name__ == '__main__':
    size = 100
    mutation_rate = 0.1
    lambda_ = size * mutation_rate
    total = 0
    for _ in range(0, 100):
        total += poisson_random_number(lambda_)
    mean = int(round(total / 99))
    print(mean)
