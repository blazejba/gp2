#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
import xml.etree.ElementTree as ET
from src.Experiment import Experiment


def main():
    experiment_name = sys.argv[1]
    evaluation_xml_path = 'eval/evaluators.xml'
    experiment_xml_path = 'exp/' + experiment_name + '.xml'
    operators_xml_path = 'eval/operators.xml'

    experiment = Experiment(ET.parse(experiment_xml_path).getroot(),
                            ET.parse(evaluation_xml_path).getroot(),
                            ET.parse(operators_xml_path).getroot(),
                            experiment_name)

    while 1:
        experiment.run()


if __name__ == '__main__':
    main()
