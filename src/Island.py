from src.utilities import decode_stdout, average_tuple
from src.Selection import Selection
from src.Reproduction import Reproduction
from src.Replacement import Replacement
from src.Migration import Migration
from src.Individual import Individual
from src.Representation import Representation
from typing import List


class Island:
    def __init__(self, pin, representation, selection, migration, replacement, reproduction, population_size, tmp_dir):
        # Island
        self.pin = pin  # personal identification num
        self.population_size = population_size  # num of individuals on a island
        self.evaluator = 'eval/' + representation.attrib['evaluator'] + '/code.py'  # this is for running an evaluator
        representation_2 = [Representation(instructions) for instructions in representation]

        # Policies
        self.selection = Selection(selection, reproduction)
        self.replacement = Replacement(replacement)
        self.reproduction = Reproduction(self.population_size, reproduction, representation_2)
        self.migration = Migration(tmp_dir, pin, migration, representation_2)

        # Population
        self.individuals = List[Individual]
        self.initiate_individuals(representation)
        self.average_fitness = 0
        self.generation = 0

    def initiate_individuals(self, representation):
        self.individuals = [Individual(representation) for _ in range(self.population_size)]

    def sort_individuals(self):
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
            new_generation += [self.reproduction.reproduce(parents)]
        # Combine generations
        self.individuals = new_generation + from_old_generation

    def next_generation(self):
        self.migration.migrate_out(self.individuals)
        self.evolve()
        self.generation += 1
        self.start_evaluations()

    def start_evaluations(self):
        for individual in self.individuals:
            individual.evaluate(self.evaluator)

    def still_evaluating(self):
        for individual in self.individuals:
            if individual.process:
                return True
        return False

    def kill_all_processes(self):
        for individual in self.individuals:
            if individual.process:
                individual.process.kill()

    def calculate_average_fitness(self):
        self.average_fitness = average_tuple([individual.fitness for individual in self.individuals])

    def print_generation_summary(self):
        print('island [', self.pin, '], fittest [', self.individuals[0].fitness, '], mean [', self.average_fitness,
              '], generation, [', self.generation, ']')

    def collect_fitness(self):
        for individual in self.individuals:
            if individual.process:
                if individual.process.poll():
                    result = individual.process.communicate()[0]
                    individual.fitness = decode_stdout(result)
                    individual.evaluated = True
                    individual.process = None
