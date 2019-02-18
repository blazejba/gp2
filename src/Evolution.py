import os
import time
import tempfile
from src.Island import Island
from src.BookKeeper import BookKeeper
from src.utilities import clean_dir


class Evolution:
	def __init__(self, experiment_xml_config, evaluators_xml_list, name):
		self.evolution_id = name
		self.book_keeper = BookKeeper(self.evolution_id)
		self.tmp_dir = tempfile.mkdtemp(dir='/tmp')

		self.max_fitness = int(experiment_xml_config.attrib['max_fitness'])
		self.max_time = int(experiment_xml_config.attrib['max_time'])
		self.max_generation = int(experiment_xml_config.attrib['max_generation'])
		self.chromosome_length = int(experiment_xml_config.attrib['chromosome_length'])

		self.islands = self.initialize_islands(experiment_xml_config, evaluators_xml_list)

	def initialize_islands(self, policies, evaluators):
		islands = []
		for pin, policy in enumerate(policies):
			population_size = int(policy.attrib['population_size'])
			evaluator = self.get_evaluator(evaluators, policy.attrib['evaluator'])
			selection = self.get_policy(policy, 'selection')
			migration = self.get_policy(policy, 'migration')
			replacement = self.get_policy(policy, 'replacement')
			reproduction = self.get_policy(policy, 'reproduction')
			islands.append(Island(pin, evaluator, selection, migration, replacement, reproduction, population_size, self.tmp_dir))
		return islands

	def get_evaluator(self, evaluators, which):
		for evaluator in evaluators:
			if evaluator.attrib['evaluator'] == which:
				return evaluator

	def get_policy(self, policies, which):
		for policy in policies:
			if policy.tag == which:
				return policy.attrib

	def termination_check(self, island):
			if island.individuals[0].fitness >= self.max_fitness != 0:
				return True, 'fitness'
			elif self.max_time < time.time() - self.book_keeper.start_t and self.max_time != 0:
				return True, 'timeout'
			elif island.generation == self.max_generation and self.max_generation != 0:
				return True, 'generation'
			else:
				return False, ''

	def run(self):
		while 1:
			for island in self.islands:
				if island.still_evaluating():
					island.collect_fitness()
					self.book_keeper.record_evaluations(1)
				else:
					self.organize_island(island)
					status, reason = self.termination_check(island)
					if status:
						self.quit_evolution(reason, island.generation)
						return self.book_keeper.final_conditions
					else:
						island.next_generation()

	def organize_island(self, island):
		island.sort_individuals()
		island.calculate_average_fitness()
		island.print_generation_summary()
		self.book_keeper.update_log(island)
		for individual in island.individuals:
			print(individual.export())

	def quit_evolution(self, reason, generation):
		for island in self.islands:
			island.kill_all_processes()
			clean_dir(self.tmp_dir)
		os.removedirs(self.tmp_dir)
		self.book_keeper.termination_printout(generation, reason)
