from os import rename, walk
from random import random, randint
from src.selection import roulette_wheel, rank_based, truncation, sort_by_scores
from src.utilities import remove_file

class MigrationPolicy(object):
	def __init__(self, tmp_dir, island_name, config):
		# General settings
		self.island_name    = island_name
		self.tmp_dir        = tmp_dir
		self.buffer_dir     = self.tmp_dir + '/' + str(self.island_name)
		self.successful_migrations  = 0
		self.total_migrations       = 0

		# Policy settings
		try:
			self.out_allowed    = config['out'] == 'true'
			self.in_allowed     = config['in'] == 'true'
		except:
			self.in_allowed     = False
			self.out_allowed    = False

		if self.in_allowed:
			try:
				self.num_of_immigrants      = int(config['immigrants'])
				self.entry_policy           = config['entry_policy']
				self.immigrant_selection    = config['selection_policy']
			except:
				self.num_of_immigrants      = 1
				self.entry_policy           = 'probabilistic'
				self.immigrant_selection    = 'roulette_wheel'

		if self.out_allowed:
			try:
				self.num_of_emigrants = int(config['emigrants'])
			except:
				self.num_of_emigrants = 1

		# Policy specific settings
		if self.entry_policy == 'periodical':
			try:
				self.period = int(config['period'])
			except:
				self.period = 5
			self.generations_since_migration = 0
		if self.entry_policy == 'probabilistic':
			try:
				self.probability    = float(config['chance'])
			except:
				self.probability    = 10

	def get_success_rate(self):
		return float((self.successful_migrations/self.total_migrations)*100) if self.total_migrations != 0 else 0

	def migrate_out(self, individuals):
		if self.out_allowed:
			for x in range(self.num_of_emigrants):
				self.create_emigrant(individuals[x])

	def select_immigrants(self, candidates):
		candidates = sort_by_scores(candidates)
		candidates_fitness = [candidate[1] for candidate in candidates]
		indexes = []
		if self.immigrant_selection == 'roulette_wheel':
			indexes = roulette_wheel(self.num_of_immigrants, candidates_fitness)
		elif self.immigrant_selection == 'rank_based':
			indexes = rank_based(self.num_of_immigrants, len(candidates))
		elif self.immigrant_selection == 'truncation':
			indexes = truncation(self.num_of_immigrants)
		elif self.immigrant_selection == 'tournament':
			indexes = []
			print('tournament to  be implemented!')
		selected_candidates = [candidates[index] for index in indexes]
		return [self.get_immigrant(candidate) for candidate in selected_candidates]

	def get_immigrant(self, candidate):
		file = open(candidate[0])
		chromosome = file.readlines()[0].split(',')
		del chromosome[len(chromosome) - 1]
		file.close()
		remove_file(candidate[0])
		return candidate[1], chromosome, True

	def create_emigrant(self, emigrant):
		buffer_file = open(self.buffer_dir, 'w+t')
		[buffer_file.write(str(gene) + ',') for gene in emigrant[1]]
		buffer_file.close()
		new_file = self.tmp_dir + '/' + str(self.island_name) + '_' + str(randint(1000, 9999)) + '_' + str(emigrant[0])
		rename(self.buffer_dir, new_file)

	def rank_migration(self, candidates):
		return [candidates[i] for i in range(self.num_of_immigrants)]

	def periodical_migration(self):
		if self.generations_since_migration == self.period:
			self.generations_since_migration = 0
			return True
		else:
			self.increase_migration_clock()
			return False

	def find_candidates(self):
		candidates = []
		for (_, _, files) in walk(self.tmp_dir):
			for file in files:
				[island, _, fitness] = [int(x) for x in file.split('_')]
				if island != self.island_name:
					path = self.tmp_dir + '/' + file
					candidates.append([path, fitness])
		return candidates

	def probabilistic_migration(self):
		R = random()
		if R * 100 < self.probability:
			return True
		return False

	def migrate_in(self):
		if self.in_allowed:
			# The entry policy
			if self.entry_policy == 'periodical':
				if not self.periodical_migration():
					return []
			elif self.entry_policy == 'probabilistic':
				if not self.probabilistic_migration():
					return []
			self.total_migrations += 1
			# Find candidates
			candidates = self.find_candidates()
			# Have enough candidates been found
			if len(candidates) >= self.num_of_immigrants:
				self.successful_migrations += 1
			# Apply selection policy
			return self.select_immigrants(candidates)
		return []

	def increase_migration_clock(self):
		if self.generations_since_migration < self.period:
			self.generations_since_migration += 1
