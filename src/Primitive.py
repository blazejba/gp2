class Primitive:
	def __init__(self, primitive_encoded):
		self.kind, self.collection, self.upper_bound, self.lower_bound = self.decode(primitive_encoded)

	def decode(self, encoded):
		open_parenthesis = encoded.find('(')
		close_parenthesis = encoded.find(')')

		kind = encoded[0:open_parenthesis]
		if kind in ['string', 'char']:
			upper_bound = None
			lower_bound = None
			collection = encoded[open_parenthesis+1:close_parenthesis].split(',')
		elif kind == 'bool':
			upper_bound = None
			lower_bound = None
			collection = [0, 1]
		elif kind == 'int':
			lower_bound, upper_bound = int(encoded[open_parenthesis+1:close_parenthesis].split(','))
			collection = [num for num in range(lower_bound, upper_bound+1)]
		elif kind == 'real':
			lower_bound, upper_bound = float(encoded[open_parenthesis+1:close_parenthesis].split(','))
			collection = None
		else:
			print("Error: something is wrong with an evaluator primitives in evaluators.xml")
			collection, upper_bound, lower_bound = [None, None, None]

		return kind, collection, upper_bound, lower_bound
