#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
import time
from src.Island import Island
import xml.etree.ElementTree as ET

PATH_EVALUATION_CONFIG = 'eval/config.xml'
PATH_EXPERIMENT_CONFIG = 'exp/' + sys.argv[1] + '.xml'


def main():
    PATH_EXPERIMENT_LOG = 'exp/logs/' + sys.argv[1] + '_' + get_date() + '.log'
    logfile = open(PATH_EXPERIMENT_LOG, 'w')
    logfile.write("configs\n")
    start_t = time.time()
    exp_xml_tree = ET.parse(PATH_EXPERIMENT_CONFIG)
    exp_xml_root = exp_xml_tree.getroot()
    max_fitness = int(exp_xml_root.attrib['max_fitness'])
    islands = []

    # INIT islands FROM experiment file
    for island in exp_xml_root:
        islands.append(Island(island.attrib, exp_xml_root.attrib))

    # OPEN processes FOR all islands
    for island in islands:
        island.open_processes()

    # CLEAN
    del exp_xml_root
    del exp_xml_tree

    while 1:
        for island in islands:
            # IF unfinished processes exist CHECK them
            if len(island.processes) > 0:
                for process in island.processes:
                    if process.poll():
                        index, fitness = decode_stdout(process.communicate()[0])
                        island.individuals[int(index)][0] = int(fitness)
                        island.individuals[int(index)][2] = True
                        island.processes.remove(process)
            # IF NOT unfinished processes exist EVOLVE and CREATE open processes
            else:
                island.sort_individuals()
                logfile.write(str(island.individuals[0]) + ',' + str(island.individuals[1]) + ',' +
                              str(island.generation) + '\n')
                if termination_check(max_fitness, island):
                    end_t = time.time()
                    print("\n")
                    print(island.generation, 'generation')
                    print(end_t - start_t, 'computation time [seconds]')
                    print(island.individuals)
                    sys.exit("Solution found.")
                island.evolve()
                island.open_processes()


def termination_check(max_fitness, island):
    if island.individuals[0][0] == max_fitness:
        return True


def decode_stdout(stdout):
    stdout = stdout.decode('ascii')
    index, fitness = [x for x in stdout.split(',')]
    return index, fitness


def print_all(islands):
    for island in islands:
        print(island + '\n')


def get_date():
    date = time.localtime()
    return str(date.tm_year) + str(date.tm_mon) + str(date.tm_mday) + \
           '_' + str(date.tm_hour) + str(date.tm_min) + str(date.tm_sec)


if __name__ == '__main__':
    main()
