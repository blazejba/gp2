import time
#from src.Island import Island


class Experiment():
	def __init__(self, experiment_xml_config, name):
		# Experiment settings
		self.max_fitness = int(experiment_xml_config.attrib['max_fitness'])
		self.max_time = int(experiment_xml_config.attrib['max_time'])
		self.genome_size = int(experiment_xml_config.attrib['genome_size'])
		self.experiment_name = name

		# Islands settings
		self.island_configs = []
		self.start_t = time.time()
		self.log = self.initialize_log()

		for island in experiment_xml_config:
			self.island_configs.append(island.attrib)

	def termination_check(self, island):
			if island.individuals[0][0] >= self.max_fitness and self.max_fitness != 0:
				print('Evolution terminated: maximum fitness has been achieved.')
				print('Generated', island.generation, 'generations in', time.time() - self.start_t, 'seconds.')
				print('Individuals of the last generation:\n')
				return True
			elif self.max_time < time.time() - self.start_t and self.max_time != 0:
				print('Evolution terminated: timeout.')
				print('Generated', island.generation, 'generations in', time.time() - self.start_t, 'seconds.')
				print('Individuals of the last generation:\n')
				return True
			return False

	def get_date_in_string(self):
		date = time.localtime()
		return str(date.tm_year) + '_' + str(date.tm_mon) + '_' + \
		       str(date.tm_mday) + '_' + str(date.tm_hour) + '_' + \
		       str(date.tm_min) + '_' + str(date.tm_sec)

	def initialize_log(self):
		path = 'exp/logs/' + self.experiment_name
		logfile = open(path + '_' + self.get_date_in_string() + '.log', 'w')
		logfile.write("configs\n")

		return logfile

	def update_log(self, island):
		self.log.write(str(island.generation) + ',' +
					   str(island.individuals[0]) + ',' +
		               str(island.individuals[1]) + '\n')