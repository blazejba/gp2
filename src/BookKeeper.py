import time
from src.utilities import get_date_in_string, average_tuple


class BookKeeper():
	def __init__(self, name):
		self.logfile = open('exp/logs/' + name + '_' + get_date_in_string() + '.log', 'w')
		self.final_conditions = []
		self.total_num_of_evaluations = 0
		self.start_t = time.time()

	def update_log(self, island):
		average_fitness = average_tuple([individual.fitness for individual in island.individuals])

		self.logfile.write(str(island.generation) + ',' + str(island.pin) + ',' +
		                   str(island.individuals[0].fitness) + ','+ str(average_fitness) + ',' +
		                   str(island.migration.migration_happened)+',\n')

	def termination_printout(self, generation, reason):
		if reason == 'timeout':
			print('Evolution terminated: timeout.')
		elif reason == 'fitness':
			print('Evolution terminated: maximum fitness has been achieved.')
		elif reason == 'generation':
			print('Evolution terminated: maximum generation has been reached.')
		evolution_time = time.time() - self.start_t
		print('Generated', generation, 'generations in', "{:.2f}".format(evolution_time), 'seconds.')
		print('Total number of evaluations', self.total_num_of_evaluations)
		print('Individuals of the last generation:\n')
		self.final_conditions = [reason, evolution_time, generation, self.total_num_of_evaluations]

	def print_migration_success_rates(self, islands):
		rates = [i.replacement_policy.migration_policy.get_success_rate() for i in islands]
		total_migrations = [island.replacement_policy.migration_policy.total_migrations for island in islands]
		print('Total migrations', [value for value in total_migrations], '.')
		print('Migration success rates', ["{:.2f} %".format(rate) for rate in rates], '.')

	def print_all_individuals(self, islands):
		for island in islands:
			print('island [ ' + str(island.island_name) + ' ]')
			for individual in island.individuals:
				print(individual)

	def record_evaluations(self, increment):
		self.total_num_of_evaluations += increment
