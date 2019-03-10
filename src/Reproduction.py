from src.Individual import Individual
from src.Tree import Tree
from random import random
from copy import deepcopy


class Reproduction:
	def __init__(self, policy):
		self.mutation_rate = float(policy.attrib['mutation_rate'])

	def reproduce(self, parents, representation):
		new_individual = Individual()
		paired_chromosomes = self.pair(self.extract_genomes(parents))
		for num in range(len(paired_chromosomes)):
			new_chromosome = self.crossover(paired_chromosomes[num], num, representation)
			new_chromosome = self.mutate(new_chromosome)
			new_individual.genome.append(new_chromosome)
		return new_individual

	def mutate(self, chromosome):
		for gene in chromosome.nodes: 	# point mutation
			if random() < self.mutation_rate:
				chromosome.mutate(node=gene)
		return chromosome

	def headless_chicken_mutation(self):
		pass

	@staticmethod
	def crossover(parent_chromosomes, index, representation):
		size, depth, constrained, primitives, unique = representation.get_tree_structure(which_tree=index)
		child_chromosome = Tree(size, depth, constrained, primitives, unique)
		child_chromosome.crossover(deepcopy(parent_chromosomes))
		return child_chromosome

	@staticmethod
	def pair(genomes):
		paired_chromosomes = [[] * len(genomes[0])]
		for genome in genomes:
			for num, chromosome in enumerate(genome):
				paired_chromosomes[num].append(chromosome)
		return paired_chromosomes

	@staticmethod
	def extract_genomes(parents):
		return [parent.genome for parent in parents]
