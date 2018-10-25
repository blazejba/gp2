#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
from src.Island import Island
import xml.etree.ElementTree as ET

PATH_EVALUATION_CONFIG = 'eval/config.xml'
PATH_EXPERIMENT_CONFIG = 'exp/' + sys.argv[1] + '.xml'


def main():
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
            island.sort_individuals()
            # IF unfinished processes exist CHECK them
            if len(island.processes) > 0:
                for process in island.processes:
                    status = process.poll()
                    if status == 1:
                        stdout = process.communicate()[0]
                        stdout = stdout.decode('ascii')
                        [index, fitness] = [x.strip() for x in stdout.split(',')]
                        island.individuals[int(index)][0] = int(fitness)
                        island.processes.remove(process)
            # IF NOT unfinished processes exist EVOLVE and CREATE open processes
            else:
                island.evolve()
                island.open_processes()
        termination_check(max_fitness, islands)


def termination_check(max_fitness, islands):
    for island in islands:
        if island.individuals[0][0] == max_fitness:
            print_all(islands)
            sys.exit()


def print_all(islands):
    for island in islands:
        print(island + '\n')


if __name__ == '__main__':
    main()
