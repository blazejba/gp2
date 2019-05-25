#!/usr/bin/env python3

'''
Copyright (c) 2019 Blazej Banaszewski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

__author__ = "Blazej Banaszewski"
__credits__ = ["John Hallam", "Blazej Banaszewski"]
__version__ = "0.9.5"
__status__ = "beta"


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

    evolutions = []
    for _ in range(num_of_evolutions):
        evolutions += ['exp/logs/' + sys.argv[1] + '_' + get_date_in_string() + '.log']
        evolution = Evolution(ET.parse(experiment_xml_path).getroot(),
                              ET.parse(evaluation_xml_path).getroot(),
                              evolutions[-1])

        evolution.run()
        del evolution

    data_processor = EvolutionMeasures(evolutions)
    data_processor.plot_fitness_graph(path=plot_path, name=experiment, runs=num_of_evolutions)

if __name__ == '__main__':
    main()
