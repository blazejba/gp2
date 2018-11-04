from random import randint, random
import subprocess


class Island(object):
    def __init__(self, config, genome_size):
        self.EVALUATION_FUNCTION = 'eval/src/' + config['eval'] + '.py'
        self.POPULATION_SIZE = int(config['size'])
        self.CROSSOVER_POINTS_NUM = int(config['crossover_points'])
        self.GENOME_SIZE = int(genome_size['genome_size'])
        self.NUM_OF_PARENTS = int(config['parents'])
        self.GA_TYPE = config['ga_type']
        if self.GA_TYPE == "ELITE":
            self.NUM_OF_ELITES = int(config['elites'])
        self.MUTATION_RATE = int(config['mutation_rate'])
        self.individuals = self.initiate_individuals()
        self.crossover_points = self.find_crossover_points()
        self.processes = []
        self.generation = 0

    def initiate_individuals(self):
        return [[0, [randint(0, 1) for _ in range(self.GENOME_SIZE)], False] for _ in range(self.POPULATION_SIZE)]

    def open_processes(self):
        for index, individual in enumerate(self.individuals):
            if individual[2]:
                continue
            genome = ''.join(str(gene) for gene in individual[1])
            self.processes.append(subprocess.Popen(["python3", self.EVALUATION_FUNCTION, genome, str(index)],
                                                   stdout=subprocess.PIPE))

    def sort_individuals(self):
        tmp_individuals = self.individuals
        self.individuals = []
        while len(tmp_individuals) > 0:
            best_fitness = 0
            best_individual = 0
            for index, individual in enumerate(tmp_individuals):
                if individual[0] > best_fitness:
                    best_fitness = individual[0]
                    best_individual = index
            self.individuals.append(tmp_individuals[best_individual])
            tmp_individuals.remove(tmp_individuals[best_individual])

    def select_propotionally(self, list):
        R = random()
        anl = self.accumulate_normalized_list(self.normalize_list(list))
        for index, entry in enumerate(anl):
            if entry >= R:
                return index

    def accumulate_normalized_list(self, normalized_list):
        anl = [normalized_list[0]]
        if len(normalized_list) >= 2:
            for index in range(1, len(normalized_list)):
                anl.append(anl[index - 1] + normalized_list[index])
        return anl

    def normalize_list(self, list):
        sum = 0
        for entry in list:
            sum += entry
        return [entry / sum for entry in list] if sum != 0 else [1] * len(list)

    def evolve(self):
        new_generation = self.replace()
        for _ in range(len(new_generation), self.POPULATION_SIZE):
            parents = self.select()
            new_generation.append(self.reproduce(parents))
        self.individuals = new_generation
        self.generation += 1

    def replace(self):
        if self.GA_TYPE == 'ELITE':
            return [self.individuals[index] for index in range(self.NUM_OF_ELITES)]

    def select(self):
        fitness_list = [individual[0] for individual in self.individuals]
        return [self.individuals[self.select_propotionally(fitness_list)][1] for _ in range(self.NUM_OF_PARENTS)]

    def reproduce(self, parents):
        return [0, self.mutate(self.crossover(parents)), False]

    def mutate(self, genome):
        for index, gene in enumerate(genome):
            R = random()
            if R*100 < self.MUTATION_RATE:
                genome[index] = 1 if gene == 0 else 0
        return genome

    def whats_mutation_rate(self, list):
        return (len(list)/self.GENOME_SIZE)*100  # [percent]

    def crossover(self, genomes):
        new_genome = []
        for section in range(self.CROSSOVER_POINTS_NUM + 1):
            choice = randint(0, self.NUM_OF_PARENTS - 1)
            new_genome += genomes[choice][self.crossover_points[section]:self.crossover_points[section+1]]
        return new_genome

    def find_crossover_points(self):
        crossover_points = []
        P = int(self.GENOME_SIZE/(self.CROSSOVER_POINTS_NUM + 1))
        for number in range(self.CROSSOVER_POINTS_NUM + 1):
            crossover_points.append(number * P)
        crossover_points.append(self.GENOME_SIZE)
        return crossover_points

#