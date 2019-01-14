from src.selection import roulette_wheel, rank_based


class SelectionPolicy(object):
	def __init__(self, selection_config, reproduction_config):
		self.policy = selection_config['policy']
		self.num_of_parents = int(reproduction_config['num_of_parents'])

	def get_fitness_list(self, individuals):
		return [individual[0] for individual in individuals]

	def select_parents(self, individuals):
		fitness_list = self.get_fitness_list(individuals)
		indexes = []
		if self.policy == 'roulette_wheel':
			indexes = roulette_wheel(fitness_list, self.num_of_parents)
		elif self.policy == 'rank_based':
			indexes = rank_based(self.num_of_parents)
		elif self.policy == 'truncation':
			print('truncation not implemented')
		elif self.policy == 'tournament':
			print('tournament not implemented')
		return [individuals[index][1] for index in indexes]
