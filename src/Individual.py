import subprocess
from src.Tree import Tree
from src.utilities import decode_stdout


class Individual:
    def __init__(self):
        self.fitness = 0
        self.process = None
        self.evaluated = False
        self.genome = [] 	# genome is represented as a forest where each tree is a chromosome

    def evaluate(self, evaluator_path, parameters):
        if not self.evaluated:
            terminal_command = ["python3", "-m", evaluator_path, self.export_genome(), parameters]
            self.process = subprocess.Popen(terminal_command, stdout=subprocess.PIPE)

    def collect_fitness(self): 	# if external evaluation completed, collect the result and update an individual
        if self.process:
            if self.process.poll():
                result = self.process.communicate()[0]
                self.fitness = decode_stdout(result)
                self.evaluated = True
                self.process = None
                return True 	# evaluation finished
        return False 	# not finished yet

    def stringify(self):
        return ''.join(letter for letter in [tree.tree_in_line() + '   ' for tree in self.genome])

    def export_genome(self):  # turn a genome (a list of trees) into a string (a list of characters)
        stringified = []
        for num, tree in enumerate(self.genome):
            stringified += tree.stringify()
            if num != len(self.genome) - 1:     # add separator between trees unless it's the last one
                stringified += '\n\n'
        return ''.join(letter for letter in stringified)

    def import_genome(self, genome_content, representation):  # turn a string into a list of trees
        for index, tree_content in enumerate(genome_content.split('\n\n')):
            size, depth, primitives, full = representation.get_tree_structure(which_tree=index)
            tree = Tree(size, depth, primitives, full)
            tree.parse(tree_content)
            self.genome += [tree]

    def instantiate(self, representation): 	# representation consists of instructions how to grow a forest
        for index in range(len(representation.forest)):
            size, depth, primitives, full = representation.get_tree_structure(which_tree=index)
            new_tree = Tree(size, depth, primitives, full)
            new_tree.grow()
            self.genome.append(new_tree)


if __name__ == '__main__':
    from src.Representation import Representation
    import xml.etree.ElementTree as ET

    representation = object
    evaluation_xml_path = 'eval/evaluators.xml'
    evaluators = ET.parse(evaluation_xml_path).getroot()
    for evaluator in evaluators:
        if evaluator.attrib['name'] == 'model_generator':
            representation = Representation(fitness_evaluator=evaluator)

    individual = Individual()
    individual.instantiate(representation)
    print(individual.export_genome())

    individual2 = Individual()
    genome = individual.export_genome()
    individual2.import_genome(genome_content=genome, representation=representation)
    print(individual2.export_genome())
