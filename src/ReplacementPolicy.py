from src.MigrationPolicy import MigrationPolicy


class ReplacementPolicy(object):
	def __init__(self, replacement_config, migration_config, tmp_dir, name, population_size):
		self.policy = replacement_config['policy']
		self.population_size = population_size
		self.migration_policy = MigrationPolicy(tmp_dir, name, migration_config)
		if self.policy == 'elitism':
			self.num_of_elites = int(replacement_config['num_of_elites'])
		elif self.policy == 'ss':
			print('steady state not implemented')

	def replace(self, individuals):
		from_old_generation = self.migration_policy.migrate_in()
		if self.policy == 'elitism':
			from_old_generation += [individuals[index] for index in range(self.num_of_elites)]
		num_of_children = self.population_size - len(from_old_generation)
		return from_old_generation, num_of_children