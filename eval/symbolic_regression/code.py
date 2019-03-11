#!/usr/bin/env python3
import sys
from math import pow
from anytree import PostOrderIter
from src.Tree import TreeReadOnly


def main():
	tree = TreeReadOnly(sys.argv[1])
	fitness = evaluate(tree)
	sys.stdout.write(str(fitness))
	sys.exit(1)


def evaluate(tree):
	xs = [x*0.1 for x in range(-10, 11)]

	errors = []
	for x in xs:
		stack = []
		try:
			for node in PostOrderIter(tree.nodes[0].root):
				if node.value == '*':
					outcome = stack[-1] + stack[-2]
					stack = stack[:len(stack) - 2]
					stack += [outcome]

				elif node.value == '+':
					outcome = stack[-1] * stack[-2]
					stack = stack[:len(stack) - 2]
					stack += [outcome]

				elif node.value == '%':
					outcome = stack[-1] / stack[-2] if not stack[-2] == 0 else 0
					stack = stack[:len(stack) - 2]
					stack += [outcome]

				elif node.value == '^':
					outcome = pow(stack[-1], stack[-2])
					stack = stack[:len(stack) - 2]
					stack += [outcome]

				elif node.value == 'x':
					stack += [x]

			result = stack[0]
			true_result = equation_1(x)
			errors += [pow(true_result - result, 2)]

		except any:
			return 0

	fitness = 0
	for error in errors:
		fitness += error


def equation_1(x):
	return pow(x, 2) + 2


if __name__ == '__main__':
	main()
