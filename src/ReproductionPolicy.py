from random import randint, random


class ReproductionPolicy(object):
	def __init__(self, population_size, reproduction_config, chromosome_length, terminal_set, function_set):
		self.num_of_crossover_points    = int(reproduction_config['crossover_points'])
		self.num_of_parents             = int(reproduction_config['num_of_parents'])
		self.mutation_rate              = float(reproduction_config['mutation_rate'])
		self.population_size            = population_size
		self.chromosome_length          = chromosome_length
		self.genotype_letters           = terminal_set + [i[0] for i in function_set]
		self.crossover_points           = self.find_crossover_points()

	def reproduce(self, parents):
		return [0, self.mutate(self.crossover(parents)), False]

	def mutate(self, genome):
		for index, gene in enumerate(genome):
			R = random()
			if R * 100 < self.mutation_rate:
				while genome[index] == gene:
					genome[index] = self.genotype_letters[randint(0, len(self.genotype_letters) - 1)]
		return genome

	def crossover(self, genomes):
		new_genome = []
		for section in range(self.num_of_crossover_points + 1):
			choice = randint(0, self.num_of_parents - 1)
			new_genome += genomes[choice][self.crossover_points[section]:self.crossover_points[section + 1]]
		return new_genome

	def find_crossover_points(self):
		crossover_points = []
		P = int(self.chromosome_length / (self.num_of_crossover_points + 1))
		for number in range(self.num_of_crossover_points + 1):
			crossover_points.append(number * P)
		crossover_points.append(self.chromosome_length)
		return crossover_points