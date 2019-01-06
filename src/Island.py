from random import randint, random
import subprocess


class Island(object):
    def __init__(self, config, genome_size, evaluation_functions):
        # Evolution settings
        self.evaluation_function_path   = 'eval/src/' + config['evaluation_function'] + '.py'
        self.population_size            = int(config['population_size'])
        self.num_of_crossover_points    = int(config['crossover_points'])
        self.num_of_parents             = int(config['parents'])
        self.mutation_rate              = int(config['mutation_rate'])
        self.replacement_strategy       = config['replacement_strategy']
        if self.replacement_strategy == "elite":
            self.num_of_elites          = int(config['elites'])
        self.genome_size = genome_size

        # Evaluation function
        for f in evaluation_functions:
            if f.attrib['name'] == config['evaluation_function']:
                self.ga_type = f[0].attrib['ea_type']
                self.dna_length = f[0].attrib['dna_length']
                self.dna_repair = f[0].attrib['dna_repair'] == 'true'
                self.dna_letters = [letter for letter in f[0].attrib['dna_letters'].split(',')]

        # EA variables
        self.generation = 0
        self.individuals = self.initiate_individuals()
        self.processes = []
        self.crossover_points = self.find_crossover_points()

        # Parallel computation variables
        self.processes = []

    def initiate_individuals(self):
        return [[0, [self.dna_letters[randint(0, len(self.dna_letters) - 1)] for _ in range(self.genome_size)], False]
                for _ in range(self.population_size)]

    def open_processes(self):
        for index, individual in enumerate(self.individuals):
            if individual[2]: # dont evaluate elites/previously evaluated
                continue
            genome = ''.join(str(gene) for gene in individual[1])
            self.processes.append(subprocess.Popen(["python3", self.evaluation_function_path, genome, str(index)],
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

    def select_proportionally(self, list):
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
        for _ in range(len(new_generation), self.population_size):
            parents = self.select()
            new_generation.append(self.reproduce(parents))
        self.individuals = new_generation
        self.generation += 1

    def replace(self):
        if self.replacement_strategy == 'elite':
            return [self.individuals[index] for index in range(self.num_of_elites)]

    def select(self):
        fitness_list = [individual[0] for individual in self.individuals]
        return [self.individuals[self.select_proportionally(fitness_list)][1] for _ in range(self.num_of_parents)]

    def reproduce(self, parents):
        return [0, self.mutate(self.crossover(parents)), False]

    def mutate(self, genome):
        for index, gene in enumerate(genome):
            R = random()
            if R*100 < self.mutation_rate:
                while genome[index] == gene:
                    genome[index] = self.dna_letters[randint(0, len(self.dna_letters) - 1)]
        return genome

    def crossover(self, genomes):
        new_genome = []
        for section in range(self.num_of_crossover_points + 1):
            choice = randint(0, self.num_of_parents - 1)
            new_genome += genomes[choice][self.crossover_points[section]:self.crossover_points[section+1]]
        return new_genome

    def find_crossover_points(self):
        crossover_points = []
        P = int(self.genome_size / (self.num_of_crossover_points + 1))
        for number in range(self.num_of_crossover_points + 1):
            crossover_points.append(number * P)
        crossover_points.append(self.genome_size)
        return crossover_points

#