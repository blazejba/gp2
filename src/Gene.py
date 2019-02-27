from random import randint
from src.Primitive import Primitive


class Gene:
	def __init__(self, role, primitive, arity=None, expression=None):
		self.role = role
		if self.role == 'f':   # f stands for function
			self.arity = arity
		self.primitive = Primitive(primitive)  # e.g. bool(), string(a, b, c), char(a, b, c), int(-1, 1), real(-1, 1)
		self.expression = self.new_gene(True) if not expression else expression

	def mutate(self):
		self.expression = self.new_gene(False)

	def new_gene(self, new=False):
		if self.primitive.kind == 'real':
			print('Real is the only primitive that doesnt use collection but upper and lower bound')
			return 0
		else:
			if not new:
				new_gene = self.primitive.collection[randint(0, len(self.primitive.collection) - 1)]
				while self.expression == new_gene:
					new_gene = self.primitive.collection[randint(0, len(self.primitive.collection) - 1)]
				return new_gene
			else:
				return self.primitive.collection[randint(0, len(self.primitive.collection) - 1)]
