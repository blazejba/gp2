#!/usr/bin/env python3

import sys

# init
genome = sys.argv[1]
individual = sys.argv[2]
fitness = 0

# evaluation
for gene in genome:
    if gene == '1':
        fitness += 1

# fill stdout
sys.stdout.write(individual + ',' + str(fitness))
sys.exit(1)
