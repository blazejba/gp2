from src.Gene import Gene
from random import random, randint
from copy import deepcopy


class Chromosome:
	def __init__(self, instructions):
		self.size = int(instructions.attrib['size'])
		if self.size == 0:
			print('restricted growth')
		self.type = instructions.tag

		self.terminals = instructions.attrib['terminals'].split(',')
		if self.type == 'tree':
			self.functions = instructions.attrib['functions']

		self.genes = self.code_genes()

	def code_genes(self):
		if self.type == 'string':
			primitive = self.terminals[randint(0, len(self.terminals) - 1)]
			return [Gene('terminal', primitive) for _ in range(self.size)]

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
			new_point = randint(1, self.size - 2)
			while new_point in points:
				new_point = randint(1, self.size - 2)
			points.append(new_point)
		return points

	def export(self):
		return [str(gene.expression) for gene in self.genes]


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
		self.ga_type = evaluator[0].attrib['ea_type']
		self.terminal_set = [letter for letter in evaluator[0].attrib['terminal_set'].split(',')]
		self.operator_set = []
		if self.ga_type == 'gp':
			self.gp_restriction = evaluator[0].attrib['restriction']
			if self.gp_restriction == 'depth':
				self.gp_max_depth = evaluator[0].attrib['max_depth']
				self.gp_method = evaluator[0].attrib['method']
			if self.gp_restriction == 'size':
				self.gp_max_size = chromosome_length

			for func in [func for func in evaluator[0].attrib['function_set'].split(',')]:
				operator, arity = func.split('_')
				self.operator_set.append([operator, int(arity)])
				
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

	def size_restricted_tree_growth(self, max_size, free_nodes):
		free_nodes -= 1
		if max_size == 0 or (random() > 0.9 and free_nodes > 0):
			return choose_random_element(self.terminal_set), max_size
		else:
			space_left = -1
			while self.tree_growth_deadlock(space_left):
				operator = choose_random_element(self.operator_set)
				space_left = max_size - operator[1]
			free_nodes += operator[1]
			max_size = space_left
			expression = [operator[0]]
			for branch in range(operator[1]):
				chromosome, max_size = self.size_restricted_tree_growth(max_size, free_nodes)
				for gene in chromosome:
					expression.append(gene)
				free_nodes -= 1
			return expression, max_size

	def unconstrained_tree_growth(self):
		print("not implemented")
		return 1

	def tree_growth_deadlock(self, space_left):
		if space_left < 0:
			return True
		for operator in self.operator_set:
			if space_left == 0 or space_left - operator[1] == 0 or space_left - operator[1] == operator[1] or space_left - operator[1] > operator[1]:
				return False
		return True

	def initiate_tree(self):
		if self.gp_restriction == 'depth':
			tree = self.depth_restricted_tree_growth(self.gp_max_depth)
		elif self.gp_restriction == 'size':
			tree = self.size_restricted_tree_growth(self.gp_max_size-1, 1)[0]
		elif self.gp_restriction == 'none':
			tree = self.unconstrained_tree_growth()
		return tree

'''