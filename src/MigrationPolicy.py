from os import rename, walk
from random import random, randint
from src.utilities import remove_file


class MigrationPolicy(object):
	def __init__(self, tmp_dir, island_name, config):
		# General settings
		self.island_name    = island_name
		self.tmp_dir        = tmp_dir
		self.buffer_dir     = self.tmp_dir + '/' + str(self.island_name)
		self.files          = ['']

		# Policy settings
		self.immigrant_selection    = config['selection']
		self.in_allowed             = config['in'] == 'true'
		if self.in_allowed:
			try:
				self.num_of_immigrants = int(config['immigrants'])
			except:
				self.num_of_immigrants = 1
		self.out_allowed = config['out'] == 'true'
		if self.out_allowed:
			try:
				self.num_of_emigrants = int(config['emigrants'])
			except:
				self.num_of_emigrants = 2
		self.policy                 = config['policy']
		self.successful_migrations  = 0
		self.total_migrations       = 0

		# Policy specific settings
		if self.policy == 'periodical':
			self.period                      = int(config['period'])
			self.generations_since_migration = 0
		if self.policy == 'probabilistic':
			self.migration_probability       = float(config['probabilistic'])

	def get_success_rate(self):
		return float((self.successful_migrations/self.total_migrations)*100)

	def migrate_out(self, individuals):
		if self.out_allowed:
			for x in range(self.num_of_emigrants):
				self.create_emigrant(individuals[x])

	def select_immigrants(self, candidates):
		if self.immigrant_selection == 'roulette_wheel':
			print('roulette_wheel')
			return candidates[0]
		elif self.immigrant_selection == 'rank':
			print('rank')
			return candidates[0]

	def create_emigrant(self, emigrant):
		buffer_file = open(self.buffer_dir, 'w+t')
		[buffer_file.write(gene + ',') for gene in emigrant[1]]
		buffer_file.close()
		new_file = self.tmp_dir + '/' + str(self.island_name) + '_' + str(randint(1000, 9999)) + '_' + str(emigrant[0])
		rename(self.buffer_dir, new_file)

	def periodical_migration(self):
		if self.generations_since_migration == self.period:
			self.total_migrations += 1
			immigrants = []
			for _ in range(self.num_of_immigrants):
				success, immigrant = self.find_immigrants()
				if not success:
					return False, []
				immigrants.append(immigrant)
			self.successful_migrations += 1
			self.generations_since_migration = 0
			return True, immigrants
		self.increase_migration_clock()
		return False, []

	def find_immigrant(self):
		candidates = []
		for (_, _, files) in walk(self.tmp_dir):
			for file in files:
				[island, _, fitness] = [int(x) for x in file.split('_')]
				if island != self.island_name: # Candidate found
					path = self.tmp_dir + '/' + file
					candidates.append([path, fitness])
		if len(candidates) == 0:
			return False, [] # Unsuccessful migration
		else:
			immigrants = self.select_immigrants(candidates)
			f = open(path)
			chromosome = f.readlines()[0].split(',')
			del chromosome[len(chromosome) - 1]
			f.close()
			remove_file(path)
			return True, [fitness, chromosome, True]

	def probabilistic_migration(self):
		R = random()
		if R * 100 < self.migration_probability:
			print('2')
		print('probabilistic migration not implemented')
		return False, []

	def migrate_in(self):
		if self.in_allowed:
			if self.policy == 'periodical':
				return self.periodical_migration()
			elif self.policy == 'probabilistic':
				return self.probabilistic_migration()
		return False, []

	def increase_migration_clock(self):
		if self.generations_since_migration < self.period:
			self.generations_since_migration += 1
