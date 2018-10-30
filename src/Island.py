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
        breeders = self.select_breeders()
        self.individuals = []
        for _ in range(self.POPULATION_SIZE):
            individual = [0, self.mutate(self.crossover(breeders))]
            self.individuals.append(individual)

    def mutate(self, genome):
        # Randomly decide which genes will be mutated based on mutation rate
        genes_to_mutate = []
        while self.whats_mutation_rate(genes_to_mutate) < self.MUTATION_RATE:
            gene = randint(0, self.GENOME_SIZE - 1)
            if gene not in genes_to_mutate:
                genes_to_mutate.append(gene)

        # Mutate selected genes
        print("how many genes are mutated", len(genes_to_mutate))
        for index in range(len(genes_to_mutate)):
            genome[genes_to_mutate[index]] = 1 if genome[genes_to_mutate[index]] == 0 else 0

        return genome

    def whats_mutation_rate(self, list):
        return (len(list)/self.GENOME_SIZE)*100

    def select_breeders(self):
        # Fitness proportionate selection
        breeders = []
        for _ in range(self.BREEDERS_NUM):
            nf = self.normalize_fitness()
            anf = self.accumulated_normalized_fitness(nf)
            R = random()
            for order, fitness in enumerate(anf):
                if fitness >= R:
                    breeders.append(self.individuals[order][1])
                    del self.individuals[order]
                    break
        return breeders

    def crossover(self, genomes):
        new_genome = []
        P = int(self.GENOME_SIZE/(self.CROSSOVER_POINTS_NUM + 1))
        crossover_points = []
        for number in range(self.CROSSOVER_POINTS_NUM + 1):
            crossover_points.append(number * P)
        crossover_points.append(self.GENOME_SIZE)
        while new_genome == genomes[0] or new_genome == genomes[1] or len(new_genome) == 0:
            new_genome = []
            for section in range(self.CROSSOVER_POINTS_NUM + 1):
                choice = randint(0, 1)
                new_genome += genomes[choice][crossover_points[section]:crossover_points[section+1]]
        return new_genome

    def accumulated_normalized_fitness(self, normd_fitness):
        anf = [normd_fitness[0]]
        if len(normd_fitness) > 2:
            for index in range(1, len(normd_fitness)):
                anf.append(anf[index - 1] + normd_fitness[index])
        return anf

    def normalize_fitness(self):
        fitness_sum = 0
        for individual in self.individuals:
            fitness_sum += individual[0]
        return [individual[0]/fitness_sum for individual in self.individuals] if fitness_sum != 0 \
            else [1] * self.POPULATION_SIZE
#