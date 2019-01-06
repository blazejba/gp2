#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
import xml.etree.ElementTree as ET
from src.Experiment import Experiment

EVALUATION_CONFIG_PATH = 'eval/config.xml'
EXPERIMENT_CONFIG_PATH = 'exp/' + sys.argv[1] + '.xml'
EXPERIMENT_LOG_PATH = 'exp/logs/' + sys.argv[1]


def main():
    # Initialize the experiment
    experiment_name = sys.argv[1]
    experiment = Experiment(ET.parse(EXPERIMENT_CONFIG_PATH).getroot(),
                            ET.parse(EVALUATION_CONFIG_PATH).getroot(),
                            experiment_name)

    while 1:
        experiment.run()


if __name__ == '__main__':
    main()
