#!/usr/bin/env python3

import sys
from src.Tree import TreeReadOnly

# init
tree = TreeReadOnly(sys.argv[1])
fitness = 0

# evaluation
for node in tree.nodes:
    if node.value == '1':
        fitness += 1

# fill stdout
sys.stdout.write(str(fitness))
sys.exit(1)
