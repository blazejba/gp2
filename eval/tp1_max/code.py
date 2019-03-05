#!/usr/bin/env python3

'''
Score board
genome_size     fitness
11              9
15              16
'''

import sys


def main():
	# init
	genome = sys.argv[1]

	# evaluation
	fitness, _ = execute_tree(genome)

	# fill stdout
	sys.stdout.write(str(fitness))
	sys.exit(1)


def execute_tree(tree):
	if len(tree) == 0:
		return 0, []
	if len(tree) > 1:
		if tree[0] == '1':
			return 1, tree[1:len(tree)]
		if len(tree) > 2:
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
		else:
			return 0, []
	else:
		return int(tree[0]), []


if __name__ == '__main__':
	main()