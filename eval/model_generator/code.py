import os
import sys
from math import sqrt, pow
from random import randint, seed
from anytree import PostOrderIter, Node
from src.utilities import get_date_in_string
from src.Tree import TreeReadOnly
from time import localtime


# Constants
ARITY = 3
RANDOM_SEED = 88
DEV_STEPS = 5


# def get_date_in_string():
#     date = localtime()
#     return str(date.tm_year) + '_' + str(date.tm_mon) + '_' + \
#            str(date.tm_mday) + '_' + str(date.tm_hour) + '_' + \
#            str(date.tm_min) + '_' + str(date.tm_sec)
#
#
# class TreeReadOnly:
#     def __init__(self, text):
#         self.nodes = []
#         self.parse(text)
#
#     def parse(self, text):  # string to tree import
#         nodes = []
#         string_nodes = text.split('\n')[:-1]
#         for string_node in string_nodes:
#             name, ptype, arity, value, parent = string_node.split(',')
#             if parent != '':
#                 for node in nodes:
#                     if node.name == parent:
#                         parent = node
#             nodes += [Node(name, ptype=ptype, arity=arity, value=value, parent=parent) if parent != ''
#                       else Node(name, ptype=ptype, arity=arity, value=value)]
#         self.nodes = nodes


class Rule:
    def __init__(self, predecessor, successors, left_context, right_context, specificity):
        self.predecessor, self.successors = predecessor, successors
        self.left_context, self.right_context = left_context, right_context
        self.specificity = specificity

    def print(self):
        print(self.left_context, ' < ', self.predecessor, ' > ', self.right_context, ' -> ', self.successors)

    def transform(self, sentence, symbol):
        if sentence[symbol] == self.predecessor:
            # left context check
            if self.left_context:
                if sentence[symbol - 1]:
                    if not sentence[symbol - 1] == self.left_context:
                        return sentence[symbol]
                else:
                    return sentence[symbol]

            # right context check
            if self.right_context:
                if sentence[symbol + 1]:
                    if not sentence[symbol + 1] == self.left_context:
                        return sentence[symbol]
                else:
                    return sentence[symbol]

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
        developmental_steps = 5
        for step in range(developmental_steps):
            for word_idx, word in enumerate(self.sentence):
                for rule in self.grammar:
                    new_word = rule.transform(self.sentence, word_idx)
                    if new_word != word:
                        break

                for letter in new_word:     # this might be a problem
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
                                          ", center=true);\n"]

                current_translation = [compound + cube_size / 2 * direction[index] for index, compound in
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
        grammar, successors, predecessor = [], [], []
        left_context, right_context = None, None
        specificity, blanks = 0, 0
        stack = []

        try:
            for node in PostOrderIter(grammar_tree.nodes[0].root):

                if node.value == '>':   # This rule has a right context
                    if stack[-1] != 'N':
                        right_context = stack[-1]
                        specificity += len(right_context)
                    blanks += 1
                    del stack[-1]
                elif node.value == '<':     # This rule has a left context
                    if stack[-1] != 'N':
                        left_context = stack[-1]
                        specificity += len(left_context)
                    blanks += 1
                    del stack[-1]
                elif int(node.arity) > 0:    # That is a predecessor node
                    predecessor = node.value if node.value != '#' else 'S'

                    # This part is about amount of successors
                    arity = int(node.arity) - blanks
                    for _ in range(arity):
                        if stack[-1] != 'N':
                            successors.append(stack[-1])
                        del stack[-1]

                    # Create new rule
                    if len(successors) > 0:
                        grammar.append(Rule(predecessor, successors, left_context, right_context, specificity))
                    stack += [predecessor]

                    # Reset rule compounds
                    successors, predecessor = [], []
                    left_context, right_context = None, None
                    specificity, blanks = 0, 0

                else:   # This is a successor node
                    stack += [node.value]

            # merge duplicates!!!!

            return grammar, True    # grammar is valid
        except:
            return [], False    # something went wrong, grammar invalid

    @staticmethod
    def count_cubes(structure):
        counter = 0
        for s in structure:
            if s == 'C':
                counter += 1
        return counter


class ModelConstructor:
    @staticmethod
    def create_scad_file(path, assembly_instructions):
        print(assembly_instructions)
        if len(assembly_instructions) > 0:
            file = open(path, 'w')
            file.write(str(assembly_instructions))
            file.close()
            return True     # report success
        else:
            return False    # report failure due to empty model


class SurfaceVolumeRatio:
    @staticmethod
    def accumulate_translations(genome):
        translations = [[0, 0, 0]]
        cube_sizes = []
        direction = [0, 0, 0]

        for letter in genome:
            if letter.isalpha():
                if letter == "Z":
                    direction = [0, 0, 1]
                if letter == "X":
                    direction = [1, 0, 0]
                if letter == "":
                    direction = [0, 1, 0]
            elif letter.isdigit():
                cube_sizes.append(int(letter))
                translations.append([int(letter) * d + translations[-1][num] for num, d in enumerate(direction)])

        return translations, cube_sizes

    def calculate_volume_surface_ratio(self, path_stl):
        triangles = self.get_triangles_from_stl(path_stl)
        volume = self.calculate_volume(triangles)
        surface = self.calculate_surface(triangles)
        return pow(volume, 0.33) / pow(surface, 0.5)

    def calculate_volume(self, triangles):    # http://chenlab.ece.cornell.edu/Publication/Cha/icip01_Cha.pdf
        volume = 0
        for triangle in triangles:
            volume += self.signed_triangle_volume(triangle[0], triangle[1], triangle[2])
        return volume

    # https://math.stackexchange.com/questions/128991/how-to-calculate-area-of-3d-triangle#128999
    def calculate_surface(self, triangles):
        surface = 0
        for triangle in triangles:
            A, B, C = triangle
            AB = self.vector_subtraction(A, B)
            AC = self.vector_subtraction(A, C)
            surface += self.triangle_surface(AB, AC)
        return surface

    @staticmethod
    def get_triangles_from_stl(path_stl):
        triangles = []
        triangle = []
        stl = open(path_stl)
        for line in stl:
            if line.find('vertex') == 6:
                point = [float(coordinate) for coordinate in line[13:-1].split(' ')]
                triangle.append(point)
                if len(triangle) == 3:
                    triangles.append(triangle)
                    triangle = []
        stl.close()
        return triangles

    @staticmethod
    def signed_triangle_volume(p1, p2, p3):
        v321 = p3[0] * p2[1] * p1[2]
        v231 = p2[0] * p3[1] * p1[2]
        v312 = p3[0] * p1[1] * p2[2]
        v132 = p1[0] * p3[1] * p2[2]
        v123 = p1[0] * p2[1] * p3[2]
        v213 = p2[0] * p1[1] * p3[2]
        return (-v321 + v231 + v312 - v132 - v213 + v123) / 6

    @staticmethod
    def vector_subtraction(A, B):
        return [B[0] - A[0], B[1] - A[1], B[2] - A[2]]

    @staticmethod
    def vector_length(x, y, z):
        return sqrt(x ^ 2 + y ^ 2 + z ^ 2)

    @staticmethod
    def triangle_surface(A, B):
        return (sqrt(
            pow(A[1] * B[2] - A[2] * B[1], 2) + pow(A[2] * B[0] - A[0] * B[2], 2) + pow(A[0] * B[1] - A[1] * B[0], 2))) / 2


def evaluate(grammar_tree):
    # Parse genome into grammar and generate assembly instructions
    l_system = LSystem(grammar_tree)

    if not l_system.success:    # if grammar parsing failed return fitness of 0
        fitness = 0
        return fitness

    l_system.sort_rules()
    l_system.rewrite()
    assembly_instruction = l_system.generate_assembly_instructions()

    # Define paths for scad and stl files
    path_scad = '/home/blaise/code/gpec/eval/model_generator/' + l_system.name + '.scad'
    path_stl = '/home/blaise/code/gpec/eval/model_generator/' + l_system.name + '.stl'

    # Construct a model from assembly instructions
    model_constructor = ModelConstructor()
    status = model_constructor.create_scad_file(path_scad, assembly_instruction)
    if status:  # Evaluate the model
        os.system('openscad -o ' + path_stl + ' ' + path_scad)
        os.remove(path=path_scad)

        evaluator = SurfaceVolumeRatio()
        fitness = evaluator.calculate_volume_surface_ratio(path_stl)
    else:   # if model generation failed return fitness of 0
        fitness = 0

    return fitness


def main():
    forest = sys.argv[1].split('\n\n')
    # forest = ['0,char,2,#,\n2,int,0,899,0\n4,int,0,81,0\n',
    #           '0,char,3,#,''\n1,string,0,N,0\n2,string,0,N,0\n3,char,3,C,0'
    #           '\n4,char,0,CD,3\n5,string,0,N,3\n6,char,3,D,3\n'
    #           '7,string,0,[DC],6\n8,char,0,N,6\n9,char,0,N,6\n']

    grammar_tree = TreeReadOnly(forest[0])
    #parameter_tree = TreeReadOnly(forest[1])

    fitness = evaluate(grammar_tree)
    sys.stdout.write(str(fitness))
    sys.exit(1)


if __name__ == "__main__":
    main()
