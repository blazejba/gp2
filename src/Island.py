from random import randint, random
import subprocess


class Island(object):
    def __init__(self, config, genome_size):
        self.EVALUATION_FUNCTION = 'eval/src/' + config['eval'] + '.py'
        self.POPULATION_SIZE = int(config['size'])
        self.BREEDERS_NUM = int(config['breeders'])
        self.CROSSOVER_POINTS_NUM = int(config['crossover_points'])
        self.GENOME_SIZE = int(genome_size['genome_size'])
        self.MUTATION_RATE = int(config['mutation_rate'])
        self.individuals = self.initiate_individuals()
        self.crossover_points = self.find_crossover_points()
        self.processes = []
        self.generation = 0

    def initiate_individuals(self):
        individuals = []
        for _ in range(self.POPULATION_SIZE):
            # [fitness, genome[], evaluated]
            individual = [0, [], False]
            for _ in range(self.GENOME_SIZE):
                individual[1].append(randint(0, 1))
            individuals.append(individual)
        return individuals

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

    def evolve(self):
        breeders = self.select_breeders()

        # Elitism
        del self.individuals[self.BREEDERS_NUM:self.POPULATION_SIZE]

        for _ in range(2, self.POPULATION_SIZE):
            individual = [0, self.mutate(self.crossover(breeders)), False]
            self.individuals.append(individual)
        self.generation += 1

    def mutate(self, genome):
        for index, gene in enumerate(genome):
            R = random()
            if R*100 < self.MUTATION_RATE:
                genome[index] = 1 if gene == 0 else 0
        return genome

    def whats_mutation_rate(self, list):
        return (len(list)/self.GENOME_SIZE)*100  # [percent]

    def select_breeders(self):
        # Truncation selection
        # Fitness proportionate selection
        breeders = []
        individuals_copy = self.individuals.copy()
        for _ in range(self.BREEDERS_NUM):
            nf = self.normalize_fitness(individuals_copy)
            anf = self.accumulated_normalized_fitness(nf)
            R = random()
            for order, fitness in enumerate(anf):
                if fitness >= R:
                    breeders.append(individuals_copy[order])
                    del individuals_copy[order]
                    break
        return breeders

    def crossover(self, breeders):
        # Proportionate selection
        genomes = [breeder[1] for breeder in breeders]
        new_genome = []
        for section in range(self.CROSSOVER_POINTS_NUM + 1):
            choice = randint(0, 1)
            new_genome += genomes[choice][self.crossover_points[section]:self.crossover_points[section+1]]
        return new_genome

    def find_crossover_points(self):
        crossover_points = []
        P = int(self.GENOME_SIZE/(self.CROSSOVER_POINTS_NUM + 1))
        for number in range(self.CROSSOVER_POINTS_NUM + 1):
            crossover_points.append(number * P)
        crossover_points.append(self.GENOME_SIZE)
        return crossover_points

    def accumulated_normalized_fitness(self, normd_fitness):
        anf = [normd_fitness[0]]
        if len(normd_fitness) >= 2:
            for index in range(1, len(normd_fitness)):
                anf.append(anf[index - 1] + normd_fitness[index])
        return anf

    def normalize_fitness(self, individuals):
        fitness_sum = 0
        for individual in individuals:
            fitness_sum += individual[0]
        return [individual[0]/fitness_sum for individual in individuals] if fitness_sum != 0 \
            else [1] * self.POPULATION_SIZE
#
