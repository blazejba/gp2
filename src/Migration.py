from os import rename, walk
from random import random
from time import time
from src.selection_methods import roulette_wheel, rank_based, truncation, tournament, sort_by_scores
from src.Individual import Individual
from src.utilities import remove_file


class Migration:
    def __init__(self, tmp_dir, island_name, policy):
        # General settings
        self.island_name = island_name
        self.tmp_dir = tmp_dir
        self.buffer_dir = self.tmp_dir + '/' + str(self.island_name)
        self.successful_migrations = 0
        self.total_migrations = 0
        self.migration_happened = False

        # Policy settings
        try:
            self.out_allowed = policy.attrib['out'] == 'true'
            self.in_allowed = policy.attrib['in'] == 'true'
        except:
            self.in_allowed = False
            self.out_allowed = False

        if self.in_allowed:  # Immigration allowance
            try:
                self.num_of_immigrants = int(policy.attrib['immigrants'])
                self.entry_policy = policy.attrib['entry_policy']
                self.immigrant_selection = policy.attrib['selection_policy']
            except:
                self.num_of_immigrants = 1
                self.entry_policy = 'probabilistic'
                self.immigrant_selection = 'roulette_wheel'

            if self.entry_policy == 'periodical':
                try:
                    self.period = int(policy.attrib['period'])
                except:
                    self.period = 5
                self.generations_since_migration = 0
            if self.entry_policy == 'probabilistic':
                try:
                    self.probability = float(policy.attrib['chance'])
                except:
                    self.probability = 10

        if self.out_allowed:  # Emigration allowance
            try:
                self.num_of_emigrants = int(policy.attrib['emigrants'])
            except:
                self.num_of_emigrants = 1

    def get_success_rate(self):
        return float((self.successful_migrations / self.total_migrations) * 100) if self.total_migrations != 0 else 0

    def migrate_out(self, individuals):
        if self.out_allowed:
            for x in range(self.num_of_emigrants):  # migrate out x best of the population
                self.create_emigrant(individuals[x])

    def select_immigrants(self, candidates, representation):
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
            indexes = tournament(self.num_of_immigrants, candidates_fitness)
        selected_candidates = [candidates[index] for index in indexes]
        return [self.get_immigrant(candidate, representation) for candidate in selected_candidates]

    @staticmethod
    def get_immigrant(candidate, representation):
        file = open(candidate[0])
        genome_encoded = file.read()
        immigrant = Individual()
        immigrant.import_genome(genome_encoded, representation)
        file.close()
        remove_file(candidate[0])
        return immigrant

    def create_emigrant(self, emigrant):
        buffer_file = open(self.buffer_dir, 'w+t')
        buffer_file.write(emigrant.export_genome())
        buffer_file.close()
        file_name = self.tmp_dir + '/' + str(self.island_name) + '_' + str(time()) + '_' + str(int(emigrant.fitness))
        rename(self.buffer_dir, file_name)  # atomic operation

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
                content = [x for x in file.split('_')]
                island, fitness = int(content[0]), float(content[2])
                if island != self.island_name:
                    path = self.tmp_dir + '/' + file
                    candidates.append([path, fitness])
        return candidates

    def probabilistic_migration(self):
        R = random()
        if R * 100 < self.probability:
            return True
        return False

    def migrate_in(self, representation):
        self.migration_happened = False
        if self.in_allowed:
            # The entry policy
            if self.entry_policy == 'periodical':
                if not self.periodical_migration():
                    return []
            elif self.entry_policy == 'probabilistic':
                if not self.probabilistic_migration():
                    return []
            self.total_migrations += 1
            self.migration_happened = True
            # Find candidates
            candidates = self.find_candidates()
            # Have enough candidates been found
            if len(candidates) >= self.num_of_immigrants:
                self.successful_migrations += 1
            # Apply selection policy
            return self.select_immigrants(candidates, representation)
        return []

    def increase_migration_clock(self):
        if self.generations_since_migration < self.period:
            self.generations_since_migration += 1
