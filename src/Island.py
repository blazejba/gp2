from random import randint, random
from src.SelectionPolicy import SelectionPolicy
from src.ReproductionPolicy import ReproductionPolicy
from src.ReplacementPolicy import ReplacementPolicy
from src.GeneticProgramming import GeneticProgramming


class Island(object):
    def __init__(self, name, configs, chromosome_length, all_evaluators, tmp_dir):
        # Evaluation function
        for f in all_evaluators:
            if f.attrib['name'] == configs.attrib['evaluator']:
                self.ga_type        = f[0].attrib['ea_type']
                self.terminal_set   = [letter for letter in f[0].attrib['terminal_set'].split(',')]
                self.operator_set   = []
                if self.ga_type == 'gp':
                    self.gp_restriction = f[0].attrib['restriction']
                    if self.gp_restriction == 'depth':
                        self.gp_max_depth   = f[0].attrib['max_depth']
                        self.gp_method      = f[0].attrib['method']
                    if self.gp_restriction == 'size':
                        self.gp_max_size    = chromosome_length

                    for func in [func for func in f[0].attrib['function_set'].split(',')]:
                        operator, arity = func.split('_')
                        self.operator_set.append([operator, int(arity)])

                self.dna_repair         = f[0].attrib['repair'] == 'true'
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
                                                         chromosome_length, self.terminal_set, self.operator_set)

        # More variables
        self.generation     = 0
        self.individuals    = self.initiate_individuals()

        self.island_name    = name
        self.processes      = []

    def depth_restricted_tree_growth(self, max_depth):
        if max_depth == 0 or (self.gp_method == 'grow' and random() < (len(self.terminal_set)/(len(self.terminal_set)+len(self.operator_set)))):
            return self.choose_random_element(self.terminal_set)
        else:
            operator = self.choose_random_element(self.operator_set)
            expression = [operator]
            for branch in range(operator[1]):
                for symbol in self.depth_restricted_tree_growth(max_depth - 1):
                    expression.append(symbol)
            return expression

    def size_restricted_tree_growth(self, max_size, free_nodes):
        free_nodes -= 1
        if max_size == 0 or (random() > 0.9 and free_nodes > 0):
            return self.choose_random_element(self.terminal_set), max_size
        else:
            space_left = -1
            while self.tree_growth_deadlock(space_left):
                operator = self.choose_random_element(self.operator_set)
                space_left = max_size - operator[1]
            free_nodes += operator[1]
            max_size = space_left
            expression = [operator[0]]
            for branch in range(operator[1]):
                chromosome, max_size = self.size_restricted_tree_growth(max_size, free_nodes)
                for gene in chromosome:
                    expression.append(gene)
                free_nodes -= 1
            return expression, max_size

    def unconstrained_tree_growth(self):
        print("not implemented")
        return 1

    def tree_growth_deadlock(self, space_left):
        if space_left < 0:
            return True
        for operator in self.operator_set:
            if space_left == 0 or space_left - operator[1] == 0 or space_left - operator[1] == operator[1] or space_left - operator[1] > operator[1]:
                return False
        return True

    def choose_random_element(self, arr):
        return arr[randint(0, len(arr)-1)]

    def initiate_tree(self):
        if self.gp_restriction == 'depth':
            tree = self.depth_restricted_tree_growth(self.gp_max_depth)
        elif self.gp_restriction == 'size':
            tree = self.size_restricted_tree_growth(self.gp_max_size-1, 1)[0]
        elif self.gp_restriction == 'none':
            tree = self.unconstrained_tree_growth()
        return tree

    def initiate_string(self):
        return [self.terminal_set[randint(0, len(self.terminal_set) - 1)] for _ in range(self.chromosome_length)]

    def initiate_individuals(self):
        if self.ga_type == 'ga':
            return [[0, self.initiate_string(), False] for _ in range(self.population_size)]
        else:
            return [[0, self.initiate_tree(), False] for _ in range(self.population_size)]

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
        print('is', self.island_name,
              'the fittest', self.individuals[0][0],
              'in gen', self.generation)

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
