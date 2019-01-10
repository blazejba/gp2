from os import rename, walk
from random import random
from src.utilities import remove_tmp


class MigrationPolicy(object):
	def __init__(self, tmp_dir, island_name, config):
		# General settings
		self.island_name        = island_name
		self.tmp_dir            = tmp_dir
		self.buffer_dir         = self.tmp_dir + '/' + str(self.island_name)
		self.migration_file     = ''

		# Policy settings
		self.in_allowed     = config['in'] == 'true'
		self.out_allowed    = config['out'] == 'true'
		self.policy         = config['policy']

		if self.policy == 'periodical':
			self.period                      = int(config['period'])
			self.generations_since_migration = 0
		if self.policy == 'probabilistic':
			self.mutation_probability        = float(config['probabilistic'])

	def migrate_out(self, individual):
		if self.out_allowed:
			file = open(self.buffer_dir, 'w+t')
			[file.write(gene + ',') for gene in individual[1]]
			file.close()
			remove_tmp(self.migration_file)
			self.migration_file = self.tmp_dir + '/' + str(self.island_name) + '_' + str(individual[0])
			rename(self.buffer_dir, self.migration_file)

	def periodical_migration(self):
		successful = False
		if self.generations_since_migration == self.period:
			for (dirpath, dirnames, filenames) in walk(self.tmp_dir):
				[island, fitness] = [int(x) for x in filenames[0].split('_')]
				if island != self.island_name:
					file = open(self.tmp_dir + '/' + filenames[0])
					chromosome = file.readlines()[0].split(',')
					del chromosome[len(chromosome) - 1]
					file.close()
					successful = True
					print('successful periodical migration')
					self.generations_since_migration = 0
					return successful, [fitness, chromosome, True]
		self.increase_migration_clock()
		print('failed periodical migration')
		return successful, []

	def probabilistic_migration(self):
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
