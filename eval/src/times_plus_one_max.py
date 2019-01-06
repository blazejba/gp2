#!/usr/bin/env python3

'''
Score board
genome_size     fitness
11              9
15              16
'''

import sys

# init
genome = sys.argv[1]
individual = sys.argv[2]
fitness = 0

# evaluation
stack = []
for symbol in genome: # reverse polish notation
	if symbol == '+':
		if len(stack) > 1:
			stack[len(stack) - 2] = stack[len(stack) - 2] + stack[len(stack) - 1]
			del stack[len(stack) - 1]
		else:
			break

	elif symbol == '*':
		if len(stack) > 1:
			stack[len(stack) - 2] = stack[len(stack) - 2] * stack[len(stack) - 1]
			del stack[len(stack) - 1]
		else:
			break
	else:
		stack.append(int(symbol))

if len(stack) == 1:
	fitness = stack[0] if stack[0] != '+' or stack[0] != '*' else 0
else:
	fitness = 0

# fill stdout
sys.stdout.write(individual + ',' + str(fitness))
sys.exit(1)


