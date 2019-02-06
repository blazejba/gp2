import os
from math import sqrt
from time import sleep
from random import randint


def main():
	genome  = "Z1X1X1Z2"
	R       = str(randint(1000, 9999))
	file    = open(R + ".scad", "w")

	translations, cubes = accumulate_translations(genome)
	for index, cube in enumerate(cubes):
		file.write("translate(" + str(translations[index]) + ") cube([" + str(cube) + "," + str(cube) + "," + str(cube) + "]);\n")

	file.close()
	os.system("openscad -o" + R + ".stl " + R + ".scad")

	sleep(2)
	triangles = get_triangles_from_stl(R)
	volume = calculate_volume(triangles)
	surface = calculate_surface(triangles)
	print(volume, surface)


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

