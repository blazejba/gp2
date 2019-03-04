import subprocess
from src.Tree import Tree


class Individual:
	def __init__(self, representation):
		self.fitness = 0
		self.process = None
		self.evaluated = False
		self.genome = self.random_genome(representation)

	def evaluate(self, evaluator):
		if not self.evaluated:
			terminal_command = ["python3", evaluator, self.export_yourself('soft')]
			self.process = subprocess.Popen(terminal_command, stdout=subprocess.PIPE)

	def collect_fitness(self):
		pass

	def export_yourself(self, how):  # turn a genome, which is a list of trees, into a string
		stringified = []
		for num, chromosome in enumerate(self.genome):
			if how == 'soft':   # soft export stringifies genes' expressions only
				stringified += chromosome.soft_export()
			elif how == 'hard':     # hard export is when all meta info is stringified
				stringified += chromosome.hard_export()
			if num != len(self.genome):     # add space between chromosomes
				stringified += ' '
		return ''.join(letter for letter in stringified)

	def import_yourself(self, genome_str):  # turn a string into a list of Chromosomes
		for imp_chromosome in genome_str.split(','):
			imp_chromosome = imp_chromosome.split(',')
			tag = imp_chromosome[0]
			size = int(imp_chromosome[1])
			genes = imp_chromosome[2:-1]
			chromosome = Chromosome(size, tag)
			chromosome.import_genes(genes)
			self.genome.append(chromosome)

	@staticmethod
	def random_genome(representation):
		return [Tree(tree.size, tree.depth, tree.unconstrained, tree.primitives_dict) for tree in representation]
