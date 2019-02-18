import subprocess
from src.Chromosome import Chromosome


class Individual:
	def __init__(self, representation):
		self.fitness = 0
		self.process = None
		self.evaluated = False
		self.genome = self.random_genome(representation) if representation else []

	def evaluate(self, evaluator):
		if not self.evaluated:
			terminal_command = ["python3", evaluator, self.export()]
			self.process = subprocess.Popen(terminal_command, stdout=subprocess.PIPE)

	def export(self):
		stringified = []
		for chromosome in self.genome:
			stringified += chromosome.export()
		return ''.join(letter for letter in stringified)

	def random_genome(self, representation):
		return [Chromosome(instructions) for instructions in representation]
