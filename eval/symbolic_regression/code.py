#!/usr/bin/env python3
import sys
from math import pow
from anytree import PostOrderIter
from src.Tree import TreeReadOnly


def main():
    tree = TreeReadOnly(sys.argv[1])
    function = sys.argv[2]
    fitness = evaluate(tree, function)
    sys.stdout.write(str(fitness))
    sys.exit(1)


def evaluate(tree, function):
    xs = [x * 1 for x in range(-10, 11)]

    errors = []
    for x in xs:
        stack = []
        try:
            for node in PostOrderIter(tree.nodes[0].root):
                if node.value == '*':
                    outcome = stack[-1] * stack[-2]
                    stack = stack[:len(stack) - 2]
                    stack += [outcome]

                elif node.value == '+':
                    outcome = stack[-1] + stack[-2]
                    stack = stack[:len(stack) - 2]
                    stack += [outcome]

                elif node.value == '%':
                    outcome = stack[-1] / stack[-2] if not stack[-2] == 0 else 0
                    stack = stack[:len(stack) - 2]
                    stack += [outcome]

                elif node.value == '^':
                    outcome = pow(stack[-2], stack[-1])
                    stack = stack[:len(stack) - 2]
                    stack += [outcome]

                elif node.value == 'x':
                    stack += [x]

                else:
                    stack += [float(node.value)]

            result = stack[0]
            true_result = equations(x=x, which=function)
            errors += [true_result - result]

        except:
            return 0

    total_squared_error = 0
    for error in errors:
        total_squared_error += abs(error)
    mse = total_squared_error / len(errors)
    fitness = 1/(1 + mse)
    return fitness


def equations(x, which):
    if which == 'quadratic':
        return pow(x, 2) + 4
    elif which == 'quartic':
        return pow(x, 4) + pow(x, 2) + 1


if __name__ == '__main__':
    main()
