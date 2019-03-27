#!/usr/bin/env python3

'''
Score board
genome_size     fitness
11              9
15              16
21				54
'''

import sys
from anytree import PostOrderIter
from src.Tree import TreeReadOnly


def main():
	tree = TreeReadOnly(sys.argv[1])
	fitness = evaluate(tree)
	sys.stdout.write(str(fitness))
	sys.exit(1)


def evaluate(tree):
	stack = []
	for node in PostOrderIter(tree.nodes[0].root):
		if node.value == '*':
			outcome = stack[-1] * stack[-2]
			stack = stack[:len(stack) - 2]
			stack += [outcome]

		elif node.value == '+':
			outcome = stack[-1] + stack[-2]
			stack = stack[:len(stack) - 2]
			stack += [outcome]

		else:
			stack += [1]
	return stack[0]


if __name__ == '__main__':
	main()
