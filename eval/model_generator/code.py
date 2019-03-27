import os
import sys
from eval.model_generator.SurfaceVolumeRatio import SurfaceVolumeRatio
from random import randint, seed
from src.utilities import get_date_in_string
from src.Tree import TreeReadOnly


# Constants
RANDOM_SEED = 88
DEV_STEPS = 6


class Rule:
    def __init__(self, predecessor, successors, left_context, right_context, specificity):
        self.predecessor, self.successors = predecessor, successors
        self.left_context = left_context if left_context else '_'
        self.right_context = right_context if right_context else '_'
        self.specificity = specificity

    def print(self):
        return str(self.left_context) + ' < ' + str(self.predecessor) + ' > ' + str(self.right_context) + ' -> ' +\
               str(self.successors)

    def transform(self, sentence, symbol):
        if sentence[symbol] == self.predecessor:
            # symbol passed left and right context check, now randomly choose one of the successors
            return self.successors[randint(0, len(self.successors) - 1)]
        else:
            return sentence[symbol]


class LSystem:
    def __init__(self, grammar_tree, parameter_tree=None):
        random_seed, self.max_size = self.parse_parameters(parameter_tree)
        self.grammar, self.success = self.parse_grammar(grammar_tree)
        seed(random_seed)
        self.sentence = 'S'
        self.name = get_date_in_string()

    def rewrite(self):
        sentence_tmp = []
        developmental_steps = DEV_STEPS
        for step in range(developmental_steps):
            for word_idx, word in enumerate(self.sentence):
                new_word = word
                for rule in self.grammar:
                    new_word = rule.transform(self.sentence, word_idx)
                    if new_word != word:
                        break

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
                direction = [sign * cube_size, 0, 0]
            elif step == 'Y':
                direction = [0, sign * cube_size, 0]
            elif step == 'Z':
                direction = [0, 0, sign * cube_size]
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
        for node in grammar_tree.nodes:
            if len(node.descendants) == 1:  # append all predecessors
                predecessor = node.value
                successor = node.descendants[0].value
                if successor == 'N':
                    continue

                exists = False
                for rule in grammar:
                    if rule.predecessor == predecessor:
                        rule.successors.append(successor)
                        exists = True
                        break

                if not exists:
                    grammar.append(Rule(predecessor, [successor], None, None, 0))

        return grammar, True


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

    if not l_system.success:    # if grammar parsing failed return fitness of 0
        fitness = 0
        return fitness

    # l_system.sort_rules()
    l_system.rewrite()
    if l_system.sentence.count('C') < 2:
        return 0
    assembly_instruction = l_system.generate_assembly_instructions()

    # Define paths for scad and stl files
    tmp_folder = '/home/blaise/code/gpec/eval/model_generator/tmp/'
    path_scad = tmp_folder + l_system.name + '.scad'
    path_stl = tmp_folder + l_system.name + '.stl'
    path_sentence = tmp_folder + l_system.name
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
