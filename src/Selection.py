from src.selection_methods import roulette_wheel, rank_based, truncation, tournament


class Selection:
	def __init__(self, policy):
		self.policy = policy.attrib['policy']
		self.num_of_parents = 2

	@staticmethod
	def get_fitness_list(individuals):
		return [individual.fitness for individual in individuals]

	def select_parents(self, individuals):
		fitness_list = self.get_fitness_list(individuals)
		indexes = []
		if self.policy == 'roulette_wheel':
			indexes = roulette_wheel(self.num_of_parents, fitness_list)
		elif self.policy == 'rank_based':
			indexes = rank_based(self.num_of_parents, len(individuals))
		elif self.policy == 'truncation':
			indexes = truncation(self.num_of_parents)
		elif self.policy == 'tournament':
			indexes = tournament(self.num_of_parents, fitness_list)
		return [individuals[index] for index in indexes]
