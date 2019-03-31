import os
import time
import tempfile
from src.Island import Island
from src.BookKeeper import BookKeeper
from src.utilities import clean_dir
from src.DiversityMeasure import DiversityMeasure


class Evolution:
    def __init__(self, islands_xml, evaluators_xml, name):
        self.evolution_id = name
        self.book_keeper = BookKeeper(self.evolution_id)
        self.tmp_dir = tempfile.mkdtemp(dir='/tmp')

        self.max_fitness = float(islands_xml.attrib['max_fitness'])
        self.max_time = int(islands_xml.attrib['max_time'])
        self.max_generation = int(islands_xml.attrib['max_generation'])

        self.islands = []
        self.initialize_islands(islands_xml, evaluators_xml)
        self.diversity_measure = DiversityMeasure()

    def initialize_islands(self, islands_xml, evaluators_xml):
        for pin, island_xml in enumerate(islands_xml):
            representation, selection, migration, reproduction, replacement, population_size, parameters = \
                self.parse_from_xml(island_xml, evaluators_xml)
            island = Island(pin, representation, parameters, selection, migration, replacement, reproduction, population_size,
                            self.tmp_dir)
            island.instantiate_individuals()
            island.start_evaluating()
            self.islands.append(island)

    def is_terminated(self, island):
        if island.individuals[0].fitness >= self.max_fitness != 0:
            return True, 'fitness'
        elif self.max_time < time.time() - self.book_keeper.start_t and self.max_time != 0:
            return True, 'timeout'
        elif island.generation == self.max_generation and self.max_generation != 0:
            return True, 'generation'
        else:
            return False, ''

    def run(self):
        while 1:
            for island in self.islands:
                if island.is_still_evaluating():
                    finished_evaluations = island.collect_fitness()
                    self.book_keeper.count_evaluations(increment=finished_evaluations)
                else:
                    self.organize_island(island)
                    status, reason = self.is_terminated(island)
                    if status:
                        self.quit_evolution(why=reason, generation=island.generation)
                        self.book_keeper.print_all_individuals(self.islands)
                        return self.book_keeper.final_conditions
                    else:
                        island.next_generation()

    def organize_island(self, island):
        island.sort_individuals()
        island.average()
        island.entropy = self.diversity_measure.entropy([individual.fitness for individual in island.individuals])
        # os.system('clear')
        island.print_generation_summary()
        self.book_keeper.update_log(island)
        self.book_keeper.print_all_individuals(self.islands)

    def quit_evolution(self, why, generation):
        for island in self.islands:
            island.kill_all_processes()
            clean_dir(self.tmp_dir)
        os.removedirs(self.tmp_dir)
        self.book_keeper.termination_printout(generation, why)

    def parse_from_xml(self, island_xml, evaluators):
        evaluator_name = island_xml.attrib['evaluator']
        parameters = island_xml.attrib['parameters'] if island_xml.attrib['parameters'] else ''
        representation = self.get_representation(evaluators=evaluators, which=evaluator_name)
        population_size = int(island_xml.attrib['population_size'])
        selection, migration, reproduction, replacement = object, object, object, object
        for policy in island_xml:
            if policy.tag == 'selection':
                selection = policy
            elif policy.tag == 'migration':
                migration = policy
            elif policy.tag == 'reproduction':
                reproduction = policy
            elif policy.tag == 'replacement':
                replacement = policy
        return representation, selection, migration, reproduction, replacement, population_size, parameters

    @staticmethod
    def get_representation(evaluators, which):
        for evaluator in evaluators:
            if evaluator.attrib['name'] == which:
                return evaluator
