from time import localtime
from os import walk
import os
import subprocess


def clean_dir(dir):
    for (dirpath, dirnames, filenames) in walk(dir):
        for name in filenames:
            path = dir + '/' + name
            remove_file(path)


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
    return [entry / total for entry in vector] if total != 0 else [1 / len(vector) for _ in range(len(vector))]


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


def open_processes(island):
    for index, individual in enumerate(island.individuals):
        if individual[2]:  # dont evaluate elites/previously evaluated
            continue
        genome = ''.join(str(gene) for gene in individual[1])
        island.processes.append(subprocess.Popen(["python3", island.evaluation_function_path, genome, str(index)],
                                                 stdout=subprocess.PIPE))


def kill_all_processes(processes):
    for process in processes:
        process.kill()