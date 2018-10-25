#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
from src.Island import Island
import xml.etree.ElementTree as ET

PATH_EVALUATION_CONFIG = "eval/config.xml"
PATH_EXPERIMENT_CONFIG = "exp/" + sys.argv[1] + ".xml"


def main():
    xml_tree = ET.parse(PATH_EXPERIMENT_CONFIG)
    xml_root = xml_tree.getroot()
    islands = []

    # INIT islands FROM experiment file
    for island in xml_root:
        islands.append(Island(island.attrib, xml_root.attrib))

    # OPEN processes FOR all islands
    for island in islands:
        island.open_processes()

    while 1:
        for island in islands:
            # IF unfinished processes CHECK them
            if len(island.processes) > 0:
                for process in island.processes:
                    status = process.poll()
                    if status == 1:
                        stdout = process.communicate()[0]
                        stdout = stdout.decode('ascii')
                        [index, fitness] = [x.strip() for x in stdout.split(',')]
                        island.individuals[int(index)][0] = int(fitness)
                        island.processes.remove(process)
            # IF NOT unfinished processes EVOLVE and CREATE open processes
            else:
                island.sort_individuals()
                print(island.individuals)
                sys.exit()
                # island.evolve()
                # island.open_processes()


if __name__ == "__main__":
    main()
