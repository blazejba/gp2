from random import random

from src.Individual import Individual
from src.Tree import Tree


class Reproduction:
    def __init__(self, policy):
        self.mutation_rate = float(policy.attrib['mutation_rate'])

    def reproduce(self, parents, representation):  # returns two individuals
        new_individual_a = Individual()
        new_individual_b = Individual()
        paired_chromosomes = self.pair(self.extract_genomes(parents))
        for num in range(len(paired_chromosomes) - 1):
            new_chromosome_a, new_chromosome_b = self.crossover(paired_chromosomes[num], num, representation)

            if random() < self.mutation_rate:
                new_chromosome_a.headless_chicken()
            new_chromosome_a = self.mutate(new_chromosome_a)

            if random() < self.mutation_rate:
                new_chromosome_b.headless_chicken()
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
    def crossover(parent_chromosomes, index, representation):
        size, depth, primitives, unique = representation.get_tree_structure(which_tree=index)
        chromosome_a = Tree(size, depth, primitives, unique)
        chromosome_b = chromosome_a.crossover(parent_chromosomes)
        return chromosome_a, chromosome_b

    @staticmethod
    def pair(genomes):
        paired_chromosomes = []
        for genome in genomes:
            pair = []
            for num, chromosome in enumerate(genome):
                pair.append(chromosome)
            paired_chromosomes.append(pair)
        return paired_chromosomes

    @staticmethod
    def extract_genomes(parents):
        return [parent.genome for parent in parents]
