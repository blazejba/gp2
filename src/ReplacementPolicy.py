from src.MigrationPolicy import MigrationPolicy


class ReplacementPolicy(object):
	def __init__(self, replacement_config, migration_config, tmp_dir, name):
		self.policy = replacement_config['policy']
		self.migration_policy = MigrationPolicy(tmp_dir, name, migration_config)
		if self.policy == 'elitism':
			self.num_of_elites = int(replacement_config['num_of_elites'])
		elif self.policy == 'ss':
			print('steady state not implemented')

	def replace(self, individuals):
		if self.policy == 'elitism':
			status, immigrant = self.migration_policy.migrate_in()
			if status:
				return [individuals[index] for index in range(self.num_of_elites - 1)] + [immigrant]
			else:
				return [individuals[index] for index in range(self.num_of_elites)]