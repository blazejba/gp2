#!/usr/bin/env python3
import sys
from math import pow

arguments = [x*0.1 for x in range(-10,11)]


def main():
	# read stdin
	genome = sys.argv[1]
	ref_num = sys.argv[2]

	# evaluate
	fitness, _ = execute_tree(genome)

	# fill stdout
	sys.stdout.write(ref_num + ',' + str(fitness))
	sys.exit(1)


def execute_tree(tree):
	if len(tree) == 0:
		return 0, []
	if len(tree) > 1:
		if tree[0] == 'x':
			return 1, tree[1:len(tree)]
		elif len(tree) > 2:
			try:
				arg_1, rest = execute_tree(tree[1:len(tree)])
			except:
				return 0, []
			try:
				arg_2, rest = execute_tree(rest)
			except:
				return 0, []

			if tree[0] == '+':
				return arg_1 + arg_2, rest
			elif tree[0] == '*':
				return arg_1 * arg_2, rest
			elif tree[0] == '%':
				return arg_1 / arg_2 if arg_2 != 0 else 0
			elif tree[0] == '^':
				return pow(arg_1, arg_2)
		else:
			return 0, []
	else:
		return int(tree[0]), []


if __name__ == '__main__':
	main()