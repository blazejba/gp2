class Representation:
    def __init__(self, fitness_evaluator):
        self.forest = []  # forest is a list of tree_structures

        for tree in fitness_evaluator:
            size = int(tree.attrib['size'])
            depth = int(tree.attrib['depth'])
            unconstrained = tree.attrib['unconstrained'] == 'True'
            primitives = self.parse_primitives(tree.attrib['primitives'])
            unique = tree.attrib['unique'] == 'true'
            tree_structure = dict(
                size=size, depth=depth, unconstrained=unconstrained, primitives=primitives, unique=unique)
            self.forest.append(tree_structure)

    @staticmethod
    def parse_primitives(primitives):
        primitive_dictionary = []
        for primitive in primitives.split(' '):
            up, low, collection, length = 0, 0, [], 1
            data_type, arity = primitive.split('_')
            open_parenthesis = data_type.find('(')
            close_parenthesis = data_type.find(')')
            ptype = data_type[0:open_parenthesis]
            if ptype in ['string', 'char']:
                collection = data_type[open_parenthesis + 1:close_parenthesis].split(',')
                if ptype == 'string':
                    arity, length = arity.split('.')
            elif ptype == 'int':
                low, up = data_type[open_parenthesis + 1:close_parenthesis].split(',')
            elif ptype == 'real':
                low, up = data_type[open_parenthesis + 1:close_parenthesis].split(',')

            primitive_dictionary.append(dict(
                ptype=ptype, arity=int(arity), collection=collection, up=float(up), low=float(low), length=int(length)))

        return primitive_dictionary

    def get_tree_structure(self, which_tree):
        return self.forest[which_tree].get('size'), self.forest[which_tree].get('depth'), \
               self.forest[which_tree].get('unconstrained'), self.forest[which_tree].get('primitives'), \
               self.forest[which_tree].get('unique')


if __name__ == '__main__':
    import xml.etree.ElementTree as ET

    representation = object
    evaluation_xml_path = '../eval/evaluators.xml'
    evaluators = ET.parse(evaluation_xml_path).getroot()
    for evaluator in evaluators:
        if evaluator.attrib['name'] == 'model_generator':
            representation = Representation(fitness_evaluator=evaluator)

    for which_tree in range(len(representation.forest)):
        print(representation.get_tree_structure(which_tree))
        print()
