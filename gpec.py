#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
import os
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
    print('\n')
    print([variable/len(data) for variable in sum_all_columns(data)])


def sum_all_columns(data):
    sum = [0] * len(data[0])
    for record in data:
        for column, variable in enumerate(record):
            if isinstance(variable, str):
                continue
            else:
                sum[column] += variable
    return sum


if __name__ == '__main__':
    main()
