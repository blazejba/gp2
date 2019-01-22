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

		self.gp = True
		if self.gp:
			self.tree_restriction           = 'max_size'
			self.terminal_set               = terminal_set
			self.function_set               = function_set
			self.point_mutation_enabled     = True
			self.headless_chicken_enabled   = True

	def reproduce(self, parents):
		return [0, self.mutate(self.crossover(parents)), False]

	def mutate(self, genome):
		if self.gp and self.headless_chicken_enabled:
			genome = self.headless_chicken_mutation(genome)
		if self.point_mutation_enabled:
			genome = self.point_mutation(genome)
		return genome

	def headless_chicken_mutation(self, genome):
		# choose a random node
		# if unconstrained
			# recursively grow a branch
		# if max_size
			# find the size of the branch
		# if max_depth
			# find the depth of the branch
		# recursively create a new branch of the same size/depth
		return genome

	def point_mutation(self, genome):
		for index, gene in enumerate(genome):
			R = random()
			if R * 100 < self.mutation_rate:
				if not self.gp or (self.gp and self.tree_restriction == 'max_size'):
					while genome[index] == gene:
						genome[index] = self.genotype_letters[randint(0, len(self.genotype_letters) - 1)]
				else:
					if self.is_function(gene):
						genome[index] = self.find_same_arity_function(gene)
					else:
						genome[index] = self.terminal_set[randint(0, len(self.terminal_set) - 1)]
		return genome

	def is_function(self, gene):
		for func in self.function_set:
			if gene == func[0]:
				return True
		return False

	def find_same_arity_function(self, func_a):
		for f in self.function_set:
			if func_a == f[0]:
				func_a_arity = f[1]
		func_b = self.function_set[randint(0, len(self.function_set) - 1)]
		while not func_a_arity == func_b[1]:
			func_b = self.function_set[randint(0, len(self.function_set) - 1)]
		return func_b[0]

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