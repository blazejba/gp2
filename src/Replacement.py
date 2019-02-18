class Replacement:
	def __init__(self, replacement_config):
		self.policy = replacement_config['policy']
		if self.policy == 'elitism':
			self.num_of_elites = int(replacement_config['num_of_elites'])

	def replace(self, from_old_generation, individuals):
		if self.policy == 'elitism':
			from_old_generation += [individuals[index] for index in range(self.num_of_elites)]
		return from_old_generation
