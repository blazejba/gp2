from random import random

from src.Individual import Individual
from src.Tree import Tree
from copy import deepcopy
from random import shuffle, sample, randint, gauss


class Reproduction:
    def __init__(self, policy):
        self.mutation_rate = float(policy.attrib['mutation_rate'])/100
        self.crossover_rate = float(policy.attrib['crossover_rate'])/100

    def reproduce(self, parents, representation):  # returns two individuals
        new_individual_a = Individual()
        new_individual_b = Individual()
        num_of_chromosomes = len(parents[0].genome)
        parent_a = parents[0]
        parent_b = parents[1]
        for num in range(num_of_chromosomes):
            if random() < self.crossover_rate:
                new_chromosome_a, new_chromosome_b = self.crossover(parent_a.genome[num], parent_b.genome[num], num, representation)
            else:
                new_chromosome_a, new_chromosome_b = deepcopy(parent_a.genome[num]), deepcopy(parent_b.genome[num])

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
        new_nodes = []
        for gene in chromosome.nodes:  # point mutation
            if random() < self.mutation_rate:
                primitive = chromosome.get_primitive(gene.ptype, gene.arity)
                if primitive.get('ptype') == 'bool':
                    gene.value = self.bool_mutation(gene.value)
                elif primitive.get('ptype') == 'char':
                    gene.value = self.char_mutation(primitive, gene.value)
                elif primitive.get('ptype') == 'real':
                    gene.value = self.real_mutation(primitive, gene.value)
                elif primitive.get('ptype') == 'int':
                    gene.value = self.int_mutation(primitive, gene.value)
                else:
                    gene.value = self.string_mutation(primitive, gene.value)
                new_nodes.append(gene)
            else:
                new_nodes.append(gene)
        chromosome.nodes = new_nodes
        return chromosome

    @staticmethod
    def crossover(parent_a, parent_b, index, representation):
        size, depth, primitives, unique = representation.get_tree_structure(which_tree=index)
        chromosome_a = Tree(size, depth, primitives, unique)
        chromosome_b = chromosome_a.crossover(parent_a, parent_b)
        return chromosome_a, chromosome_b

    @staticmethod
    def bool_mutation(current_value):
        return 1 if current_value == 0 else 0

    @staticmethod
    def char_mutation(primitive, current_value):
        collection = primitive.get('collection')
        value = current_value
        while len(collection) > 1:
            value = sample(collection, 1)[0]
            if value != current_value:
                break
        return value

    @staticmethod
    def real_mutation(primitive, current_value):
        low = primitive.get('low')
        up = primitive.get('up')
        while True:
            value = gauss(current_value, (abs(low) + abs(up)) / 100)
            if value > low or value < up:
                break
        return value

    @staticmethod
    def int_mutation(primitive, current_value):
        low = primitive.get('low')
        up = primitive.get('up')
        while True:
            value = current_value - 1 if randint(0, 1) == 0 else current_value + 1
            if value > low or value < up:
                break
        return value

    @staticmethod
    def string_mutation(primitive, current_value):
        collection = primitive.get('collection')
        current_length = len(current_value)

        available_operations = ['add', 'remove', 'change', 'shuffle']
        if current_length == primitive.get('length'):
            available_operations.remove('add')
        elif current_length == 1:
            available_operations.remove('remove')
            available_operations.remove('shuffle')

        mutation_choice = available_operations[randint(0, len(available_operations) - 1)]

        if mutation_choice == 'add':
            added_value = sample(collection, 1)[0]
            position = randint(0, current_length - 1)
            value = current_value[:position] + added_value + current_value[position:]
            return value

        elif mutation_choice == 'remove':
            return current_value.replace(current_value[randint(0, current_length - 1)], '')

        elif mutation_choice == 'change':
            position = randint(0, current_length - 1)
            while True:
                new_char = sample(collection, 1)[0]
                if new_char != current_value[position]:
                    break
            new_string = current_value[:position] + new_char + current_value[position + 1:]
            return new_string
        else:
            value = current_value
            shuffle(value)
            return value
