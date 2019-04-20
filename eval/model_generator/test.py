import subprocess
import sys

stl = '2019_4_8_18_55_4.stl'
path_fitness = '/home/blaise/code/gpec/eval/model_generator/tmp/results/'
terminal_command = ['freecad', '-c', '/home/blaise/code/gpec/eval/model_generator/Constructor.py', stl]
subprocess.call(terminal_command)
file = open(path_fitness + stl[:-4], 'r')
file.close()
print(sys.stdout)