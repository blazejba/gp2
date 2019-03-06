from src.Individual import Individual
from src.Tree import Tree
from random import random


class Reproduction:
	def __init__(self, population_size, reproduction_config):
		self.crossover_points_num = int(reproduction_config.attrib['crossover_points'])
		self.mutation_rate = float(reproduction_config.attrib['mutation_rate'])
		self.population_size = population_size

	def reproduce(self, parents, representation):
		new_individual = Individual()
		paired_chromosomes = self.pair(self.extract_genomes(parents))
		for num, chromosome in enumerate(parents.genome):
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

	def crossover(self, parent_chromosomes, index, representation):
		# remember about deep copying
		size, depth, unconstrained, primitives = representation.get_tree_structure(which_tree=index)
		child_chromosome = Tree(size, depth, unconstrained, primitives)
		child_chromosome.crossover(parent_chromosomes)
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
