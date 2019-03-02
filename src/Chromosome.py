from src.Gene import Gene
from src.Tree import Tree
from random import random, randint
from copy import deepcopy


class Chromosome:
	def __init__(self, length, primitives):
		self.length = int(length)
		if self.length == 0:
			print('restricted growth')



		if self.type == 'tree':
			self.genes = self.code_genes(terminals.split(','), functions.split(',')) if terminals and functions else []
		else:
			self.genes = self.code_genes(terminals.split(',')) if terminals else []

	def import_genes(self, genes):
		for gene in genes:
			open_parenthesis = gene.find('(')
			close_parenthesis = gene.find(')')
			role_split = gene.split('_')

			if len(role_split) > 1:
				role = 'f'
				arity = int(role_split[1])
			else:
				role = 's'
				arity = None
			expression = gene[open_parenthesis + 1:close_parenthesis]

			self.genes.append(Gene(role, gene, arity=arity, expression=expression))

	def code_genes(self, terminals, functions=None):
		return [Gene(self.select_primitive()) for _ in range(self.length)]

	def select_primitive(self):
		# if root -> look for a function
			# if there is no function -> look for a terminal
		#

	def mutate(self, mutation_rate):
		for gene in self.genes:
			if random() * 100 < mutation_rate:
				gene.mutate()

	def crossover(self, chromosomes, num_of_points=None):
		if self.type == 'string':
			self.ga_crossover(chromosomes, num_of_points)
		elif self.type == 'tree':
			self.gp_crossover()

	def ga_crossover(self, chromosomes, num_of_points):
		new_genes = []
		crossover_points = self.find_crossover_points(num_of_points)
		parent = randint(0, len(chromosomes) - 1)
		while len(new_genes) < len(self.genes):
			new_genes.append(deepcopy(chromosomes[parent].genes[len(new_genes)]))
			if len(new_genes) in crossover_points:
				new_parent = randint(0, len(chromosomes) - 1)
				while new_parent == parent:
					new_parent = randint(0, len(chromosomes) - 1)
				parent = new_parent
		self.genes = new_genes

	def gp_crossover(self):
		print('do crossover for trees')

	def find_crossover_points(self, num_of_points):
		points = []
		for _ in range(num_of_points):
			new_point = randint(1, self.length - 2)
			while new_point in points:
				new_point = randint(1, self.length - 2)
			points.append(new_point)
		return points

	def soft_export(self):
		return [str(gene.expression) for gene in self.genes]

	def hard_export(self):
		string = ''.join('t' if self.type == 'tree' else 's')
		string += ''.join(',' + str(self.length))
		for gene in self.genes:
			arity = '.' + gene.arity if gene.role == 'f' else ''
			string += ''.join(',' + gene.primitive.kind + '(' + str(gene.expression) + arity + ')')
		return string


'''
	def find_same_arity_function(self, func_a):
		for f in self.function_set:
			if func_a == f[0]:
				func_a_arity = f[1]
		func_b = self.function_set[randint(0, len(self.function_set) - 1)]
		while not func_a_arity == func_b[1]:
			func_b = self.function_set[randint(0, len(self.function_set) - 1)]
		return func_b[0]
'''

'''			
	def depth_restricted_tree_growth(self, max_depth):
		if max_depth == 0 or (self.gp_method == 'grow' and random() < (len(self.terminal_set)/(len(self.terminal_set)+len(self.operator_set)))):
			return choose_random_element(self.terminal_set)
		else:
			operator = choose_random_element(self.operator_set)
			expression = [operator]
			for branch in range(operator[1]):
				for symbol in self.depth_restricted_tree_growth(max_depth - 1):
					expression.append(symbol)
			return expression

	def unconstrained_tree_growth(self):
		print("not implemented")
		return 1



	def initiate_tree(self):
		if self.gp_restriction == 'depth':
			tree = self.depth_restricted_tree_growth(self.gp_max_depth)
		elif self.gp_restriction == 'size':
			tree = self.size_restricted_tree_growth(self.gp_max_size-1, 1)[0]
		elif self.gp_restriction == 'none':
			tree = self.unconstrained_tree_growth()
		return tree

'''