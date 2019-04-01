import time
from src.utilities import average_tuple


class BookKeeper:
    def __init__(self, name):
        self.logfile = open(name, 'w+')
        self.final_conditions = []
        self.total_num_of_evaluations = 0
        self.start_t = time.time()

    def update_log(self, island):
        fitness_list = [individual.fitness for individual in island.individuals]
        average_fitness = average_tuple(fitness_list)

        self.logfile.write(str(island.generation) + ',' + str(island.pin) + ',' +
                           str(island.individuals[0].fitness) + ',' + str(average_fitness) + ',' +
                           str(island.migration.migration_happened) + ',' + str(island.diversity_measure.entropy) + '\n')

    def termination_printout(self, generation, reason):
        print('')
        if reason == 'timeout':
            print('Evolution terminated: timeout.')
        elif reason == 'fitness':
            print('Evolution terminated: maximum fitness has been achieved.')
        elif reason == 'generation':
            print('Evolution terminated: maximum generation has been reached.')
        evolution_time = time.time() - self.start_t
        print('Generated', generation, 'generations in', "{:.2f}".format(evolution_time), 'seconds.')
        print('Total number of evaluations', self.total_num_of_evaluations)
        print('\nIndividuals of the last generation:')
        self.final_conditions = [evolution_time, generation, self.total_num_of_evaluations]

    def count_evaluations(self, increment):
        self.total_num_of_evaluations += increment

    @staticmethod
    def print_migration_success_rates(islands):
        rates = [i.replacement_policy.migration_policy.get_success_rate() for i in islands]
        total_migrations = [island.replacement_policy.migration_policy.total_migrations for island in islands]
        print('Total migrations', [value for value in total_migrations], '.')
        print('Migration success rates', ["{:.2f}".format(rate) for rate in rates], '.')

    @staticmethod
    def print_all_individuals(islands):
        for island in islands:
            print('island [ ' + str(island.pin) + ' ]')
            for individual in island.individuals:
                print("[{:.2f}]".format(individual.shared_fitness), "[{:.2f}]".format(individual.fitness), individual.stringify())
                # individual.genome[0].print()
