#!/usr/bin/env python3

import sys

genome = sys.argv[1]
individual = sys.argv[2]
fitness = 0

for gene in genome:
    if gene == '1':
        fitness += 1

sys.stdout.write(individual + ',' + str(fitness))
sys.exit(1)
