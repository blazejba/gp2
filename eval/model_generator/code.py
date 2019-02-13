import os
import re
import sys
from math import sqrt, pow
from random import randint, seed
from src.utilities import get_date_in_string


class LSystem():
	def __init__(self, grammar, max_size, rnd_seed):
		seed(rnd_seed)
		self.max_size = max_size
		self.grammar = grammar
		self.structure = self.grow()

	def grow(self):
		structure = 'S'
		structure_tmp = []
		while self.count_cubes(structure) < self.max_size and structure != ['']:
			for branch in [self.transform(s) for s in structure]:
				for symbol in branch:
					structure_tmp.append(symbol)
			structure = structure_tmp
			structure_tmp = []
		return structure

	def transform(self, symbol):
		for rule in self.grammar:
			if rule[0] == symbol:
				return rule[randint(1, len(rule) - 1)]
		return ''

	def count_cubes(self, structure):
		counter = 0
		for s in structure:
			if s == 'C':
				counter += 1
		return counter


def decode_stdin(inp):
	comma_separated = re.sub('.n', '', inp).split(',')
	return [rule.split('.') for rule in comma_separated[0:-2] if len(rule) > 1], int(comma_separated[-2]), int(comma_separated[-1])


def execute_growth_instruction(instruction, name, rnd_seed):
	seed(rnd_seed)
	file = open(name + ".scad", "w")
	current_translation = [0, 0, 0]
	direction = [1, 0, 0]
	saved_translations = []

	for step in instruction:
		if step == 'C':
			cube_size = randint(1, 5)
			file.write("translate(" + str(current_translation) + ") cube(" + str(cube_size) + ", center=true);\n")
			current_translation = [compound + cube_size/2*direction[index] for index, compound in enumerate(current_translation)]
		elif step == 'D':
			direction = [randint(-1, 1), randint(-1, 1), randint(-1, 1)]
		elif step == '[':
			saved_translations.append(current_translation)
		elif step == ']':
			current_translation = saved_translations[-1]
			del saved_translations[-1]
		print("STEP " + step + " DIR " + str(direction) + " CTR " + str(current_translation) + " CUBE " + str(cube_size))

	file.close()


def main():
	genome = "S.C[DCC][DCC].n.n.n.n,C.CC[DC].n.n.n.n,20,1"
	#genome = sys.argv[1]
	individual = sys.argv[2]

	grammar, size, rnd_seed = decode_stdin(genome)
	l_system = LSystem(grammar, size, rnd_seed)

	name = get_date_in_string()
	execute_growth_instruction(l_system.structure, name, rnd_seed)

	os.system("openscad -o" + name + ".stl " + name + ".scad")

	triangles = get_triangles_from_stl(name)
	volume = calculate_volume(triangles)
	surface = calculate_surface(triangles)
	fitness = pow(volume, 0.33)/pow(surface, 0.5)

	print(volume, surface, fitness)
	sys.stdout.write(individual + ',' + str(fitness))
	sys.exit(1)


def accumulate_translations(genome):
	translations = [[0, 0, 0]]
	cube_sizes   = []
	direction    = [0, 0, 0]

	for letter in genome:
		if letter.isalpha():
			if letter == "Z":
				direction = [0, 0, 1]
			if letter == "X":
				direction = [1, 0, 0]
			if letter == "":
				direction = [0, 1, 0]
		elif letter.isdigit():
			cube_sizes.append(int(letter))
			translations.append([int(letter)*d + translations[-1][num] for num, d in enumerate(direction)])

	return translations, cube_sizes


#http://chenlab.ece.cornell.edu/Publication/Cha/icip01_Cha.pdf
def calculate_volume(triangles):
	volume = 0
	for triangle in triangles:
		volume += signed_triangle_volume(triangle[0], triangle[1], triangle[2])
	return volume

#https://math.stackexchange.com/questions/128991/how-to-calculate-area-of-3d-triangle#128999
def calculate_surface(triangles):
	surface = 0
	for triangle in triangles:
		A, B, C = triangle
		AB = vector_subtraction(A, B)
		AC = vector_subtraction(A, C)
		surface += triangle_surface(AB, AC)
	return surface


def get_triangles_from_stl(name):
	triangles = []
	triangle = []
	stl = open(name + '.stl')
	for line in stl:
		if line.find('vertex') == 6:
			point = [float(coordinate) for coordinate in line[13:-1].split(' ')]
			triangle.append(point)
			if len(triangle) == 3:
				triangles.append(triangle)
				triangle = []
	stl.close()
	return triangles


def signed_triangle_volume(p1, p2, p3):
	v321 = p3[0]*p2[1]*p1[2]
	v231 = p2[0]*p3[1]*p1[2]
	v312 = p3[0]*p1[1]*p2[2]
	v132 = p1[0]*p3[1]*p2[2]
	v123 = p1[0]*p2[1]*p3[2]
	v213 = p2[0]*p1[1]*p3[2]
	return (-v321+v231+v312-v132-v213+v123)/6


def vector_subtraction(A, B):
	return [B[0] - A[0], B[1] - A[1], B[2] - A[2]]


def vector_length(x, y, z):
	return sqrt(x^2 + y^2 + z^2)


def triangle_surface(A, B):
	return (sqrt(pow(A[1] * B[2] - A[2] * B[1], 2) + pow(A[2] * B[0] - A[0] * B[2], 2) + pow(A[0] * B[1] - A[1] * B[0], 2))) / 2


if __name__ == "__main__":
	main()

