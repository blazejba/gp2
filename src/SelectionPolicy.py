from random import random
from src.utilities import normalize_vector, accumulate_vector


class SelectionPolicy(object):
	def __init__(self, selection_config, reproduction_config):
		self.policy = selection_config['policy']
		self.num_of_parents = int(reproduction_config['num_of_parents'])

	def get_fitness_list(self, individuals):
		return [individual[0] for individual in individuals]

	def select_one(self, population_fitness):
		if self.policy == 'roulette_wheel':
			R = random()
			anl = accumulate_vector(normalize_vector(population_fitness))
			for index, entry in enumerate(anl):
				if entry >= R:
					return index
		elif self.policy == 'rank':
			print('rank not implemented')
		elif self.policy == 'truncation':
			print('truncation not implemented')
		elif self.policy == 'tournament':
			print('tournament not implemented')

	def select_parents(self, individuals):
		fitness_list = self.get_fitness_list(individuals)
		return [individuals[self.select_one(fitness_list)][1] for _ in range(self.num_of_parents)]