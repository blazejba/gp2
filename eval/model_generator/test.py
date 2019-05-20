import subprocess
from time import time
from os import listdir
import io
import sys


path_fitness = '/home/blaise/code/gpec/eval/model_generator/tmp/results/'
path_stl = '/home/blaise/code/gpec/eval/model_generator/tmp/stls/'

for stl in listdir(path_stl):
    start = time()
    f = open('/tmp/' + stl[:-4], 'w')
    tmp_pipe = io.TextIOWrapper(f, encoding='utf8', newline='')
    terminal_command = ['freecad', '-c', '/home/blaise/code/gpec/eval/model_generator/Constructor.py', stl]
    subprocess.call(terminal_command, stdout=tmp_pipe)
    file = open(path_fitness + stl[:-4], 'r')
    fitness = file.read()
    previously_evaluated = stl.split('_')[0]
    if fitness != previously_evaluated:
        print(fitness, '!=', previously_evaluated, '    ', stl)
    file.close()
