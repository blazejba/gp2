from random import random

from src.Individual import Individual
from src.Tree import Tree


class Reproduction:
    def __init__(self, policy):
        self.mutation_rate = float(policy.attrib['mutation_rate'])/100

    def reproduce(self, parents, representation):  # returns two individuals
        new_individual_a = Individual()
        new_individual_b = Individual()
        num_of_chromosomes = len(parents[0].genome)
        parent_a = parents[0]
        parent_b = parents[1]
        for num in range(num_of_chromosomes):
            new_chromosome_a, new_chromosome_b = self.crossover(parent_a.genome[num], parent_b.genome[num], num, representation)

            if random() < self.mutation_rate:
                new_chromosome_a.headless_chicken()
            else:
                new_chromosome_a = self.mutate(new_chromosome_a)

            if random() < self.mutation_rate:
                new_chromosome_b.headless_chicken()
            else:
                new_chromosome_b = self.mutate(new_chromosome_b)

            new_individual_a.genome.append(new_chromosome_a)
            new_individual_b.genome.append(new_chromosome_b)

        return [new_individual_a, new_individual_b]

    def mutate(self, chromosome):
        for gene in chromosome.nodes:  # point mutation
            if random() < self.mutation_rate:
                chromosome.mutate(node=gene)
        return chromosome

    @staticmethod
    def crossover(parent_a, parent_b, index, representation):
        size, depth, primitives, unique = representation.get_tree_structure(which_tree=index)
        chromosome_a = Tree(size, depth, primitives, unique)
        chromosome_b = chromosome_a.crossover(parent_a, parent_b)
        return chromosome_a, chromosome_b

