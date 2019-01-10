from os import rename, walk
from src.utilities import remove_tmp


class MigrationPolicy(object):
	def __init__(self, tmp_dir, island_name, config):
		# General settings
		self.island_name        = island_name
		self.tmp_dir            = tmp_dir
		self.buffer_dir         = self.tmp_dir + '/' + str(self.island_name)
		self.migration_file     = ''

		# Policy settings
		configs = [x for x in config.split(',')]
		self.in_allowed                     = configs[0] == 'true'
		self.out_allowed                    = configs[1] == 'true'
		self.policy                         = configs[2]
		self.period                         = int(configs[3])
		self.generations_since_migration    = 0

	def migrate_out(self, individual):
		if self.out_allowed:
			file = open(self.buffer_dir, 'w+t')
			[file.write(gene + ',') for gene in individual[1]]
			file.close()
			remove_tmp(self.migration_file)
			self.migration_file = self.tmp_dir + '/' + str(self.island_name) + '_' + str(individual[0])
			rename(self.buffer_dir, self.migration_file)

	def migrate_in(self):
		successful = False
		for (dirpath, dirnames, filenames) in walk(self.tmp_dir):
			[island, fitness] = [int(x) for x in filenames[0].split('_')]
			if island != self.island_name:
				file = open(self.tmp_dir + '/' + filenames[0])
				chromosome = file.readlines()[0].split(',')
				del chromosome[len(chromosome) - 1]
				file.close()
				successful = True
				print('success')
				return successful, [fitness, chromosome, True]
		print('fail')
		return successful, []

	def increase_migration_clock(self):
		if self.generations_since_migration < self.period:
			self.generations_since_migration += 1
