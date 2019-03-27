#!/usr/bin/env python3

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "1.0.0"
__status__ = "Prototype"


import sys
import xml.etree.ElementTree as ET
from src.Evolution import Evolution
from src.utilities import get_date_in_string
from src.EvolutionMeasures import EvolutionMeasures


def main():
    experiment = sys.argv[1]
    num_of_evolutions = int(sys.argv[2])
    evaluation_xml_path = 'eval/evaluators.xml'
    experiment_xml_path = 'exp/' + experiment + '.xml'
    plot_path = 'exp/plots/' + experiment + '.png'

    time = []
    gens = []
    evals = []
    evolutions = []
    for _ in range(num_of_evolutions):
        evolutions += ['exp/logs/' + sys.argv[1] + '_' + get_date_in_string() + '.log']
        evolution = Evolution(ET.parse(experiment_xml_path).getroot(),
                              ET.parse(evaluation_xml_path).getroot(),
                              evolutions[-1])

        means = evolution.run()
        time += [means[0]]
        gens += [means[1]]
        evals += [means[2]]
        del evolution

    data_processor = EvolutionMeasures(evolutions)
    data_processor.summarize_experiment(time=time, generations=gens, evaluations=evals)
    data_processor.plot_fitness_graph(path=plot_path, name=experiment, runs=num_of_evolutions)


if __name__ == '__main__':
    main()
