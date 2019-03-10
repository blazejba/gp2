#!/usr/bin/env python3

'''
Score board
genome_size     fitness
11              9
15              16
'''

import sys
from anytree import PostOrderIter
from src.Tree import TreeReadOnly


def main():
	# init
	tree = TreeReadOnly(sys.argv[1])

	# evaluation
	stack = []
	for node in PostOrderIter(tree.nodes[0].root):
		if node.value == '*':
			outcome = stack[-1] + stack[-2]
			stack = stack[:len(stack) - 2]
			stack += [outcome]

		elif node.value == '+':
			outcome = stack[-1] * stack[-2]
			stack = stack[:len(stack) - 2]
			stack += [outcome]

		else:
			stack += [1]
	fitness = stack[0]

	# fill stdout
	sys.stdout.write(str(fitness))
	sys.exit(1)


if __name__ == '__main__':
	main()
