#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
import xml.etree.ElementTree as ET
from src.Evolution import Evolution


def main():
    experiment_name = sys.argv[1]
    num_of_evolutions = int(sys.argv[2])
    evaluation_xml_path = 'eval/evaluators.xml'
    experiment_xml_path = 'exp/' + experiment_name + '.xml'

    data = []
    for _ in range(num_of_evolutions):
        evolution = Evolution(ET.parse(experiment_xml_path).getroot(),
                              ET.parse(evaluation_xml_path).getroot(),
                              experiment_name)

        data.append(evolution.run())
        del evolution

    process_data(data)


def process_data(data):
    headers = ['\nreasons ratio: ', 'mean evaluation time: ', 'mean generations: ', 'mean evaluations: ']
    units = ['', ' seconds', '', '']
    values = [str('%.1f' % (variable/len(data))) for variable in sum_all_columns(data)]
    [print(headers[index] + values[index] + units[index]) for index in range(len(headers))]


def sum_all_columns(data):
    total = [0] * len(data[0])
    for record in data:
        for column, variable in enumerate(record):
            if isinstance(variable, str):
                pass
            else:
                total[column] += variable
    return total


if __name__ == '__main__':
    experiment_name = 'one_max_1is'
    evaluation_xml_path = 'eval/evaluators.xml'
    experiment_xml_path = 'exp/' + experiment_name + '.xml'
    evolution = Evolution(ET.parse(experiment_xml_path).getroot(),
                          ET.parse(evaluation_xml_path).getroot(),
                          experiment_name)

    evolution.run()
    # island = evolution.islands[0]
    # island.start_evaluating()
    # while island.is_still_evaluating():
    #     island.collect_fitness()
    # for individual in island.individuals:
    #     print(individual.fitness)
    #     individual.genome[0].print()
