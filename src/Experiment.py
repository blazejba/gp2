import sys
import time
from src.Island import Island
from src.utilities import decode_stdout, get_date_in_string


class Experiment():
	def __init__(self, experiment_xml_config, evaluators_xml_config, name):
		self.start_t = time.time()

		# Experiment settings
		self.max_fitness        = int(experiment_xml_config.attrib['max_fitness'])
		self.max_time           = int(experiment_xml_config.attrib['max_time'])
		self.genome_size        = int(experiment_xml_config.attrib['genome_size'])
		self.experiment_name    = name

		# Islands settings
		self.island_configs = []
		self.islands        = self.initialize_islands(experiment_xml_config, evaluators_xml_config)

		# Logs
		self.log = self.initialize_log()

	def initialize_islands(self, experiment, evaluators):
		return [Island(island.attrib, self.genome_size, evaluators) for island in experiment]

	def termination_check(self, island):
			if island.individuals[0][0] >= self.max_fitness and self.max_fitness != 0:
				print('Evolution terminated: maximum fitness has been achieved.')
				print('Generated', island.generation, 'generations in', time.time() - self.start_t, 'seconds.')
				print('Individuals of the last generation:\n')
				self.print_all_individuals()
				return True

			elif self.max_time < time.time() - self.start_t and self.max_time != 0:
				print('Evolution terminated: timeout.')
				print('Generated', island.generation, 'generations in', time.time() - self.start_t, 'seconds.')
				print('Individuals of the last generation:\n')
				self.print_all_individuals()
				return True

			return False

	def initialize_log(self):
		path = 'exp/logs/' + self.experiment_name
		logfile = open(path + '_' + get_date_in_string() + '.log', 'w')
		logfile.write("configs\n")

		return logfile

	def update_log(self, island):
		self.log.write(str(island.generation) + ',' +
					   str(island.individuals[0]) + ',' +
		               str(island.individuals[1]) + '\n')

	def print_all_individuals(self):
		for island in self.islands:
			for individual in island.individuals:
				print(individual)

	def run(self):
			for island in self.islands:
				if len(island.processes) > 0: # Collect stdout from unfinished processes if they exists
					for process in island.processes:
						if process.poll():
							index, fitness = decode_stdout(process.communicate()[0])
							island.individuals[int(index)][0] = int(fitness)
							island.individuals[int(index)][2] = True
							island.processes.remove(process)
				else:
					island.sort_individuals()
					self.update_log(island)
					if self.termination_check(island):
						sys.exit()
					else:
						island.evolve()
						island.open_processes()