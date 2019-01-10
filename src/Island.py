from random import randint
from src.MigrationPolicy import MigrationPolicy
from src.SelectionPolicy import SelectionPolicy
from src.ReproductionPolicy import ReproductionPolicy
from src.ReplacementPolicy import ReplacementPolicy
import subprocess


class Island(object):
    def __init__(self, name, config, chromosome_length, evaluation_functions, tmp_dir):
        # Evaluation function
        for f in evaluation_functions:
            if f.attrib['name'] == config['evaluator']:
                self.ga_type            = f[0].attrib['ea_type']
                self.dna_length         = f[0].attrib['dna_length']
                self.dna_repair         = f[0].attrib['dna_repair'] == 'true'
                self.genotype_letters   = [letter for letter in f[0].attrib['dna_letters'].split(',')]

        # Evolution settings
        self.evaluation_function_path   = 'eval/src/' + config['evaluator'] + '.py'
        self.population_size            = int(config['population_size'])
        self.reproduction_policy        = ReproductionPolicy(int(config['population_size']),
                                                             int(config['crossover_points']),
                                                             int(config['parents']),
                                                             int(config['mutation_rate']),
                                                             chromosome_length,
                                                             self.genotype_letters)

        self.replacement_policy         = config['replacement_policy']
        self.selection_policy           = SelectionPolicy(config['selection_policy'], int(config['parents']))
        self.migration_policy           = MigrationPolicy(tmp_dir, name, config['migration_policy'])
        self.replacement_policy         = ReplacementPolicy(config['replacement_policy'],
                                                            config['num_of_elites'],
                                                            tmp_dir,
                                                            name,
                                                            config['migration_policy'])

        self.chromosome_length          = chromosome_length
        self.island_name                = name

        # EA variables
        self.generation         = 0
        self.individuals        = self.initiate_individuals()

        # Parallel computation variables
        self.processes = []
        self.open_processes()

    def initiate_individuals(self):
        return [[0, [self.genotype_letters[randint(0, len(self.genotype_letters) - 1)] for _ in range(self.chromosome_length)], False]
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

    def evolve(self):
        new_generation = self.replacement_policy.replace(self.individuals)
        for _ in range(len(new_generation), self.population_size):
            parents = self.selection_policy.select_parents(self.individuals)
            new_generation.append(self.reproduction_policy.reproduce(parents))
        self.individuals = new_generation
        self.generation += 1
#