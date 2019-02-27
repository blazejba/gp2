class PrimitiveDictionary:
	def __init__(self):
		self.dictionary = []

	def add_primitive(self, name, arity, collection, up_bound=None, low_bound=None):
		self.dictionary.append({'key': 1, 'name': name, 'arity': arity, 'collection': collection, 'up_bound': up_bound, 'low_bound': low_bound})

	def find_primitive(self):
		pass