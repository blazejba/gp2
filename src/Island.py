from src.utilities import average_tuple
from src.Selection import Selection
from src.Reproduction import Reproduction
from src.Replacement import Replacement
from src.Migration import Migration
from src.Individual import Individual
from src.Representation import Representation


class Island:
    def __init__(self, pin, evaluator, selection, migration, replacement, reproduction, population_size, tmp_dir):
        # Island
        self.pin = pin  # personal identification num
        self.population_size = population_size  # num of individuals on a island
        self.evaluator = 'eval.' + evaluator.attrib['name'] + '.code'  # this is for running an evaluator
        self.representation = Representation(fitness_evaluator=evaluator)

        # Policies
        self.selection = Selection(selection)
        self.replacement = Replacement(replacement)
        self.reproduction = Reproduction(self.population_size, reproduction)
        self.migration = Migration(tmp_dir, pin, migration)

        # Population
        self.individuals = []
        self.average_fitness = 0
        self.generation = 0

    def instantiate_individuals(self):
        while self.population_size > len(self.individuals):
            individual = Individual()
            individual.instantiate(self.representation)
            self.individuals.append(individual)

    def sort_individuals(self):     # from the fittest to the least fit
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
        immigrants = self.migration.migrate_in()
        # Replacement
        from_old_generation = self.replacement.replace(immigrants, self.individuals)
        # Breed children
        new_generation = []
        offspring = self.population_size - len(from_old_generation)
        for _ in range(offspring):
            # Selection
            parents = self.selection.select_parents(self.individuals)
            # Reproduction
            new_generation += [self.reproduction.reproduce(parents, self.representation)]
        # Combine generations
        self.individuals = new_generation + from_old_generation

    def next_generation(self):
        self.migration.migrate_out(self.individuals)
        self.evolve()
        self.generation += 1
        self.start_evaluating()

    def start_evaluating(self):
        for individual in self.individuals:
            individual.evaluate(self.evaluator)

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
        print('island [', self.pin, '], fittest [', self.individuals[0].fitness, '], mean [', self.average_fitness,
              '], generation, [', self.generation, ']')

    def collect_fitness(self):
        for individual in self.individuals:
            individual.collect_fitness()


if __name__ == '__main__':
    pass
