from typing import List


class Representation:
	def __init__(self, instructions):
		terminals = instructions.attrib['terminals'].split(',')
		functions = instructions.attrib['functions'].split(',')
		self.length = instructions.attrib['size']
		self.primitives_dict = List[dict]

		primitives = terminals + functions
		for primitive in primitives:
			data_type, arity = primitive.split('_')
			open_parenthesis = data_type.find('(')
			close_parenthesis = data_type.find(')')
			name = data_type[0:open_parenthesis]
			up_bound, low_bound = None, None

			if name in ['string', 'char']:
				collection = data_type[open_parenthesis + 1:close_parenthesis].split(',')
			elif name == 'bool':
				collection = [0, 1]
			elif name == 'int':
				low_bound, up_bound = int(data_type[open_parenthesis + 1:close_parenthesis].split(','))
				collection = [num for num in range(low_bound, up_bound + 1)]
			elif name == 'real':
				low_bound,  = float(data_type[open_parenthesis + 1:close_parenthesis].split(','))
				collection = None
			else:
				print("Error: something is wrong with an evaluator primitives in evaluators.xml")
				collection, up_bound, low_bound = [None, None, None]

			self.add_primitive(name, arity, collection, up_bound, low_bound)
		print('representation', self.primitives_dict)

	def add_primitive(self, name, arity, collection, up_bound, low_bound):
		self.primitives_dict.append(
			dict(name=name, arity=arity, collection=collection, up_bound=up_bound, low_bound=low_bound))

	def find_primitive(self):
		pass
