from src.Individual import Individual


class Reproduction:
	def __init__(self, population_size, reproduction_config, representation):
		self.crossover_points_num = int(reproduction_config['crossover_points'])
		self.mutation_rate = float(reproduction_config['mutation_rate'])
		self.population_size = population_size
		self.representation = representation

	def reproduce(self, parents):
		new_individual = Individual(self.representation)
		paired_chromosomes = self.pair(self.extract_genomes(parents))
		for num, chromosome in enumerate(new_individual.genome):
			chromosome.crossover(paired_chromosomes[num], self.crossover_points_num)
			chromosome.mutate(self.mutation_rate)
		return new_individual

	def pair(self, genomes):
		paired_chromosomes = [[] * len(genomes[0])]
		for genome in genomes:
			for num, chromosome in enumerate(genome):
				paired_chromosomes[num].append(chromosome)
		return paired_chromosomes

	def extract_genomes(self, parents):
		return [parent.genome for parent in parents]
