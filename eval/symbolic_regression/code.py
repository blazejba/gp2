#!/usr/bin/env python3
import sys
from math import pow, e
from anytree import PostOrderIter
from src.Tree import TreeReadOnly


def main():
    tree = TreeReadOnly(sys.argv[1])
    fitness = evaluate(tree)
    sys.stdout.flush()
    sys.stdout.write(str(fitness))
    sys.exit(1)


def evaluate(tree):
    xs = [x * 1 for x in range(-10, 11)]

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

                else:
                    stack += [float(node.value)]

            result = stack[0]
            true_result = equation_1(x)
            errors += [true_result - result]

        except:
            return 0

    total_squared_error = 0
    for error in errors:
        total_squared_error += abs(error)
    mse = total_squared_error / len(errors)
    fitness = 1/(1 + mse)
    return fitness


def equation_1(x):
    return pow(x, 2) + 4


if __name__ == '__main__':
    main()
