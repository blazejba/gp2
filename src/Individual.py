import subprocess
from src.Tree import Tree
from src.utilities import decode_stdout


class Individual:
	def __init__(self):
		self.fitness = 0
		self.process = None
		self.evaluated = False
		self.genome = [] 	# genome is represented as a forest where each tree is a chromosome

	def evaluate(self, evaluator): 	# start and external evaluator with genome as an argument
		if not self.evaluated:
			terminal_command = ["python3", evaluator, self.export_genome()]
			self.process = subprocess.Popen(terminal_command, stdout=subprocess.PIPE)

	def collect_fitness(self): 	# if external evaluation has been completed, collect the result and update an individual
		if self.process:
			if self.process.poll():
				result = self.process.communicate()[0]
				self.fitness = decode_stdout(result)
				self.evaluated = True
				self.process = None

	def export_genome(self):  # turn a genome (a list of trees) into a string (a list of characters)
		stringified = []
		for num, tree in enumerate(self.genome):
			stringified += tree.stringify()
			if num != len(self.genome):     # add separator between trees unless it's the last one
				stringified += '\n\n'
		return ''.join(letter for letter in stringified)

	def import_yourself(self, genome_str, representation):  # turn a string into a list of trees
		for index, tree in enumerate(genome_str.split('\n\n')):
			size, depth, unconstrained, primitives = representation.tree_structure(tree=index)
			tree = Tree(size, depth, unconstrained, primitives)
			self.genome += [tree]

	def instantiate(self, representation): 	# representation consists of instructions how to grow a forest
		self.genome = [Tree(tree.size, tree.depth, tree.unconstrained, tree.primitives_dict) for tree in representation]


if __name__ == '__main__':
	pass
