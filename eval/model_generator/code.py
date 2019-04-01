import os
import sys
from eval.model_generator.SurfaceVolumeRatio import SurfaceVolumeRatio
from random import seed
from src.utilities import get_date_in_string
from src.Tree import TreeReadOnly


# Constants
RANDOM_SEED = 88
DEV_STEPS = 8


class Rule:
    def __init__(self, predecessor, successor, left_context, right_context, specificity):
        self.predecessor, self.successor = predecessor, successor
        self.left_context = left_context if left_context else '_'
        self.right_context = right_context if right_context else '_'
        self.specificity = specificity

    def print(self):
        return str(self.left_context) + ' < ' + str(self.predecessor) + ' > ' + str(self.right_context) + ' -> ' +\
               str(self.successor)


class LSystem:
    def __init__(self, grammar_tree, parameter_tree=None):
        random_seed, self.max_size = self.parse_parameters(parameter_tree)
        self.grammar = self.parse_grammar(grammar_tree)
        seed(random_seed)
        self.sentence = 'S'
        self.name = get_date_in_string()

    def find_rule(self, symbol):
        for rule in self.grammar:
            if rule.predecessor == symbol:
                return rule
        return None

    def rewrite(self):
        sentence_tmp = []
        developmental_steps = DEV_STEPS
        for step in range(developmental_steps):
            for word_idx, word in enumerate(self.sentence):
                rule = self.find_rule(word)
                if not rule:
                    continue
                new_word = rule.successor
                for letter in new_word:
                    sentence_tmp.append(letter)

            if sentence_tmp == self.sentence:
                return

            self.sentence = sentence_tmp
            sentence_tmp = []

    def sort_rules(self):   # sorts rules in descending manner according to their specificity
        grammar_tmp = self.grammar
        self.grammar = []

        while len(grammar_tmp) > 0:
            max_specificity_rule = None
            for index, rule in enumerate(grammar_tmp):
                if index == 0:
                    max_specificity_rule = rule
                else:
                    if max_specificity_rule.specificity < rule.specificity:
                        max_specificity_rule = rule

            self.grammar.append(max_specificity_rule)
            grammar_tmp.remove(max_specificity_rule)

    def save_sentence_and_grammar(self, path):
        file = open(path, 'w')
        for letter in self.sentence:
            file.write(letter)
        file.write('\n')
        for rule in self.grammar:
            file.write(rule.print() + '\n')
        file.close()

    def generate_assembly_instructions(self):
        current_translation = [0, 0, 0]
        direction = [1, 0, 0]
        sign = 1
        saved_translations = []
        cube_size = 1

        assembly_instructions = []

        for step in self.sentence:
            if step == 'C':
                assembly_instructions += ["translate(" + str(current_translation) + ") cube(" + str(cube_size) +
                                          ", center=true);"]

                current_translation = [compound + cube_size * direction[index] for index, compound in
                                       enumerate(current_translation)]
            elif step == '+':
                sign = 1
            elif step == '-':
                sign = -1
            elif step == 'X':
                direction = [sign, 0, 0]
            elif step == 'Y':
                direction = [0, sign, 0]
            elif step == 'Z':
                direction = [0, 0, sign]
            elif step == '[':
                saved_translations.append(current_translation)
            elif step == ']' and len(saved_translations) > 0:
                current_translation = saved_translations[-1]
                del saved_translations[-1]

        return assembly_instructions

    @staticmethod
    def parse_parameters(parameters_tree=None):
        rnd_seed = RANDOM_SEED if parameters_tree else parameters_tree
        developmental_step = DEV_STEPS if parameters_tree else parameters_tree
        return rnd_seed, developmental_step

    @staticmethod
    def parse_grammar(grammar_tree):
        grammar = []
        predecessors = ['S', 'C', 'X', 'Y', 'Z', '[', ']', '+', '-']
        predecessor_pointer = 0
        for node in grammar_tree.nodes:
            if node.ptype == 'root':
                continue
            successor = node.value
            if 'N' in successor:
                continue
            grammar.append(Rule(predecessors[predecessor_pointer], successor, None, None, 0))
            predecessor_pointer += 1
        return grammar


class ModelConstructor:
    @staticmethod
    def create_scad_file(path, assembly_instructions):
        if len(assembly_instructions) > 0:
            file = open(path, 'w')
            for line in assembly_instructions:
                file.write(str(line) + '\n')
            file.close()
            return True     # report success
        else:
            return False    # report failure due to empty model


def evaluate(grammar_tree):
    # Parse genome into grammar and generate assembly instructions
    l_system = LSystem(grammar_tree)
    l_system.rewrite()
    if not l_system.sentence.count('C') > 0:
        return 0
    assembly_instruction = l_system.generate_assembly_instructions()

    # Define paths for scad and stl files
    tmp_folder = '/home/blaise/code/gpec/eval/model_generator/tmp/'
    path_scad = tmp_folder + 'scads/' + l_system.name + '.scad'
    path_stl = tmp_folder + 'stls/' + l_system.name + '.stl'
    path_sentence = tmp_folder + 'rules/' + l_system.name
    l_system.save_sentence_and_grammar(path_sentence)

    # Construct a model from assembly instructions
    model_constructor = ModelConstructor()
    status = model_constructor.create_scad_file(path_scad, assembly_instruction)
    if status:  # Evaluate the model
        os.system('openscad -o ' + path_stl + ' ' + path_scad)
        evaluator = SurfaceVolumeRatio()
        fitness = evaluator.calculate_volume_surface_ratio(path_stl)

    else:   # if model generation failed return fitness of 0
        fitness = 0
    return fitness


def main():
    forest = sys.argv[1].split('\n\n')
    grammar_tree = TreeReadOnly(forest[0])

    fitness = evaluate(grammar_tree)
    sys.stdout.write(str(fitness))
    sys.exit(1)


if __name__ == "__main__":
    main()
