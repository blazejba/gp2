#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
from src.Island import Island
from src.Experiment import Experiment
import xml.etree.ElementTree as ET


EVALUATION_CONFIG_PATH = 'eval/config.xml'
EXPERIMENT_CONFIG_PATH = 'exp/' + sys.argv[1] + '.xml'
EXPERIMENT_LOG_PATH = 'exp/logs/' + sys.argv[1]


def main():
    # Initialize the experiment
    experiment = Experiment(ET.parse(EXPERIMENT_CONFIG_PATH).getroot(), sys.argv[1])

    # Create and populate the islands, then start artificial evolution
    islands = init_islands(experiment, ET.parse(EVALUATION_CONFIG_PATH).getroot())

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
                experiment.update_log(island)

                # Terminate the experiment if time or fitness condition has been reached
                # Otherwise keep on evolving
                if experiment.termination_check(island):
                    print_all(islands)
                    sys.exit()
                else:
                    island.evolve()
                    island.open_processes()


def init_islands(experiment, evaluation_functions):
    islands = []

    # INIT islands FROM experiment file
    for island in experiment.island_configs:
        islands.append(Island(island, experiment.genome_size, evaluation_functions))

    # OPEN processes
    for island in islands:
        island.open_processes()

    return islands


def decode_stdout(stdout):
    stdout = stdout.decode('ascii')
    index, fitness = [x for x in stdout.split(',')]
    return index, fitness


def print_all(islands):
    for island in islands:
        for individual in island.individuals:
            print(individual)


if __name__ == '__main__':
    main()
