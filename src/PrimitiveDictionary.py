from typing import List


class PrimitiveDictionary:
	dictionary: List[dict]

	def add_primitive(self, name, arity, collection, up_bound=None, low_bound=None):
		self.dictionary.append(
			dict(key=1, name=name, arity=arity, collection=collection, up_bound=up_bound, low_bound=low_bound))

	def find_primitive(self):
		pass
