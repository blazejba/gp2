from random import randint
from src.SelectionPolicy import SelectionPolicy
from src.ReproductionPolicy import ReproductionPolicy
from src.ReplacementPolicy import ReplacementPolicy


class Island(object):
    def __init__(self, name, configs, chromosome_length, evaluation_functions, tmp_dir):
        # Evaluation function
        for f in evaluation_functions:
            if f.attrib['name'] == configs.attrib['evaluator']:
                self.ga_type            = f[0].attrib['ea_type']
                self.dna_length         = f[0].attrib['dna_length']
                self.dna_repair         = f[0].attrib['dna_repair'] == 'true'
                self.genotype_letters   = [letter for letter in f[0].attrib['dna_letters'].split(',')]
        self.evaluation_function_path   = 'eval/' + configs.attrib['evaluator'] + '/code.py'

        # Evolution settings
        self.chromosome_length  = chromosome_length
        self.population_size    = int(configs.attrib['population_size'])

        # Policies
        for c in configs:
            if c.tag == 'migration':
                migration_config = c.attrib
            elif c.tag == 'replacement':
                replacement_config = c.attrib
            elif c.tag == 'reproduction':
                reproduction_config = c.attrib
            elif c.tag == 'selection':
                selection_config = c.attrib
        if not migration_config and not reproduction_config and not replacement_config and not selection_config:
            print('[config error] migration, reproduction, replacement or selection config missing or incomplete.')

        self.selection_policy       = SelectionPolicy(selection_config, reproduction_config)
        self.replacement_policy     = ReplacementPolicy(replacement_config, migration_config, tmp_dir,
                                                        name, self.population_size)
        self.reproduction_policy    = ReproductionPolicy(self.population_size, reproduction_config,
                                                         chromosome_length, self.genotype_letters)

        # More variables
        self.generation     = 0
        self.individuals    = self.initiate_individuals()
        self.island_name    = name
        self.processes      = []

    def initiate_individuals(self):
        return [[0, [self.genotype_letters[randint(0, len(self.genotype_letters) - 1)] for _ in range(self.chromosome_length)], False]
                for _ in range(self.population_size)]

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
        # Replacement
        from_old_generation, num_of_children = self.replacement_policy.replace(self.individuals)
        # Selection
        parents = self.selection_policy.select_parents(self.individuals)
        # Reproduction
        new_generation = [self.reproduction_policy.reproduce(parents) for _ in range(num_of_children)]
        # New generation
        self.individuals = new_generation + from_old_generation
        self.generation += 1