class GeneticProgramming(object):
	def __init__(self, evaluator_config, chromosome_length):
		self.terminal_set       = evaluator_config[0].attrib['terminal_set']

		self.operator_set       = []
		for func in [func for func in evaluator_config[0].attrib['function_set'].split(',')]:
			operator, arity = func.split('_')
			self.operator_set.append([operator, int(arity)])

		self.growth_restriction = evaluator_config[0].attrib['restriction']
		if self.growth_restriction == 'size':
			self.max_size = chromosome_length
		elif self.growth_restriction == 'depth':
			self.max_depth  = int(evaluator_config[0].attrib['max_depth'])
			self.method     = evaluator_config[0].attrib['method']