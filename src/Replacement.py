class Replacement:
	def __init__(self, policy):
		self.policy = policy.attrib['policy']
		if self.policy == 'elitism':
			self.num_of_elites = int(policy.attrib['num_of_elites'])

	def replace(self, from_old_generation, individuals):
		if self.policy == 'elitism':
			from_old_generation += self.find_n_fittest(individuals, self.num_of_elites)
		return from_old_generation

	@staticmethod
	def find_n_fittest(individuals, n):
		fittest = []
		tmp_individuals = individuals
		fitness = [individual.fitness for individual in tmp_individuals]
		for _ in range(n):
			max_index = fitness.index(max(fitness))
			fittest.append(tmp_individuals[max_index])
			del tmp_individuals[max_index]
			del fitness[max_index]
		return fittest
