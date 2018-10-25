from random import randint, random
import subprocess


class Island(object):
    def __init__(self, config, genome_size):
        self.EVALUATION_FUNCTION = 'eval/src/' + config['eval'] + '.py'
        self.POPULATION_SIZE = int(config['size'])
        self.NUM_OF_BREEDERS = int(config['breeders'])
        self.CROSSOVER_POINTS = int(config['crossover_points'])
        self.GENOME_SIZE = int(genome_size['genome_size'])
        self.individuals = self.initiate_individuals()
        self.processes = []

    def initiate_individuals(self):
        individuals = []
        for _ in range(self.POPULATION_SIZE):
            individual = [0, []]
            for _ in range(self.GENOME_SIZE):
                individual[1].append(randint(0, 1))
            individuals.append(individual)
        return individuals

    def open_processes(self):
        for index, individual in enumerate(self.individuals):
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

    def evolve(self):
        # Fitness proportionate selection
        breeders = []
        for _ in range(self.NUM_OF_BREEDERS):
            nf = self.normalize_fitness()
            anf = self.accumulated_normalized_fitness(nf)
            R = random()
            for order, fitness in enumerate(anf):
                if fitness >= R:
                    breeders.append(self.individuals[order][1])
                    del self.individuals[order]

    def crossover(self, genome1, genome2):
        new_genome = []

        return new_genome

    def accumulated_normalized_fitness(self, normalized_fitness):
        anf = [normalized_fitness[0]]
        return [anf.append(normalized_fitness[index-1] + normalized_fitness[index]) for index in range(1, len(anf)-1)]

    def normalize_fitness(self):
        fitness_sum = 0
        for individual in self.individuals:
            fitness_sum += individual[0]
        nf = []
        return [nf.append(individual[0]/fitnessSum) for individual in self.individuals]