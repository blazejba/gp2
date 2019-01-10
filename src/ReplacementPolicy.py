from src.MigrationPolicy import MigrationPolicy


class ReplacementPolicy(object):
	def __init__(self, policy, num_of_elites, tmp_dir, name, migration_policy):
		self.policy = policy
		self.migration_policy = MigrationPolicy(tmp_dir, name, migration_policy)
		if self.policy == 'elite':
			self.num_of_elites = int(num_of_elites)
		elif self.policy == 'ss':
			print('steady state not implemented')

	def replace(self, individuals):
		if self.policy == 'elite':
			if self.migration_policy.in_allowed:
				if self.migration_policy.generations_since_migration == self.migration_policy.period:
					status, immigrant = self.migration_policy.migrate_in()
					if status:
						self.migration_policy.generations_since_migration = 0
						return [individuals[index] for index in range(self.num_of_elites - 1)] + [immigrant]
			self.migration_policy.increase_migration_clock()
			return [individuals[index] for index in range(self.num_of_elites)]