from src.Individual import Individual
from src.Migration import Migration
from src.Replacement import Replacement
from src.Representation import Representation
from src.Reproduction import Reproduction
from src.Selection import Selection
from src.utilities import average_tuple


class Island:
    def __init__(self, pin, evaluator, parameters, selection, migration, replacement, reproduction, population_size, tmp_dir):
        # Island
        self.pin = pin  # personal identification num
        self.population_size = population_size  # num of individuals on a island
        self.evaluator = 'eval.' + evaluator.attrib['name'] + '.code'  # this is for running an evaluator
        self.parameters = parameters
        self.representation = Representation(fitness_evaluator=evaluator)

        # Policies
        self.selection = Selection(policy=selection)
        self.replacement = Replacement(policy=replacement)
        self.reproduction = Reproduction(policy=reproduction)
        self.migration = Migration(tmp_dir, pin, policy=migration)

        # Population
        self.individuals = []
        self.average_fitness = 0
        self.generation = 0
        self.entropy = 0

    def instantiate_individuals(self):
        while self.population_size > len(self.individuals):
            individual = Individual()
            individual.instantiate(self.representation)
            self.individuals.append(individual)

    def sort_individuals(self):  # from the fittest to the least fit
        tmp_individuals = self.individuals
        self.individuals = []
        while len(tmp_individuals) > 0:
            best_fitness = 0
            best_individual = 0
            for index, individual in enumerate(tmp_individuals):
                if individual.fitness > best_fitness:
                    best_fitness = individual.fitness
                    best_individual = index
            self.individuals.append(tmp_individuals[best_individual])
            tmp_individuals.remove(tmp_individuals[best_individual])

    def evolve(self):
        # Migration
        immigrants = [] if self.generation == 0 else self.migration.migrate_in(self.representation)
        # Replacement
        from_old_generation = self.replacement.replace(immigrants, self.individuals)
        # Breed children
        new_generation = []
        offspring = self.population_size - len(from_old_generation)
        while True:
            # Selection
            parents = self.selection.select_parents(self.individuals)
            # Reproduction
            children = self.reproduction.reproduce(parents, self.representation)
            new_generation += children if offspring - len(new_generation) > 1 else [children[0]]
            if len(new_generation) >= offspring:
                break
        # Combine generations
        self.individuals = new_generation + from_old_generation

    def next_generation(self):
        self.migration.migrate_out(self.individuals)
        self.evolve()
        self.generation += 1
        self.start_evaluating()

    def start_evaluating(self):
        for individual in self.individuals:
            individual.evaluate(self.evaluator, self.parameters)

    def is_still_evaluating(self):
        for individual in self.individuals:
            if individual.process:
                return True
        return False

    def kill_all_processes(self):
        for individual in self.individuals:
            if individual.process:
                individual.process.kill()

    def average(self):
        self.average_fitness = average_tuple([individual.fitness for individual in self.individuals])

    def print_generation_summary(self):
        print('island [', self.pin, '], fittest [', '{0:.2f}'.format(self.individuals[0].fitness), '], entropy [',
              '{0:.2f}'.format(self.entropy), '], mean [', '{0:.2f}'.format(self.average_fitness),
              '], generation [', self.generation, ']')

    def collect_fitness(self):
        evaluations_finished = 0
        for individual in self.individuals:
            status = individual.collect_fitness()
            if status:
                evaluations_finished += 1
        return evaluations_finished


if __name__ == '__main__':
    pass
