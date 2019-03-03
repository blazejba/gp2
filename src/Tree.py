#!/usr/bin/env python3

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.importer import JsonImporter
from random import randint, sample, uniform, shuffle


class Tree:
    def __init__(self, size, depth, constrain, primitives):
        if not constrain:
            self.max_size = randint(5, size)
            self.max_depth = randint(1, depth)
        else:
            self.max_size = size if size != 0 else 999
            self.max_depth = depth if depth != 0 else 999
        print('Depth', self.max_depth, 'Size', self.max_size)
        self.primitive_dict = primitives
        self.nodes = []

    def grow(self):  # first grow all the nodes then fill the remaining branches with leafs
        size, depth, num = [0] * 3
        free_branches = []

        # Growing nodes
        while True:
            size, depth, num, free_branches = self.expand(size, depth, num, free_branches)
            if size >= self.max_size or depth >= self.max_depth or len(free_branches) == 0:
                break

        # Growing leafs
        while 0 < len(free_branches):
            num, free_branches = self.grow_leafs(num, free_branches)

    def grow_leafs(self, num, free_branches):  # grow a random terminal node
        ptype, value = self.grow_leaf()
        parent = free_branches[randint(0, len(free_branches) - 1)]
        self.nodes.append(Node(str(num), ptype=ptype, arity=0, value=value, parent=parent))
        free_branches.remove(parent)
        num += 1
        return num, free_branches

    def expand(self, size, depth, num, free_branches):  # expand tree by growing a new node
        space_left = self.max_size - size
        ptype, arity, value = self.grow_node(space_left)
        if num == 0:
            self.nodes.append(Node(str(num), ptype=ptype, arity=arity, value=value))
        else:
            parent = free_branches[randint(0, len(free_branches) - 1)]
            self.nodes.append(Node(str(num), ptype=ptype, arity=arity, value=value, parent=parent))
            free_branches.remove(parent)
        free_branches += [self.nodes[-1]] * arity
        size += arity + 1 if num == 0 else arity
        depth = depth if self.nodes[-1].depth < depth else self.nodes[-1].depth + 1
        num += 1
        return size, depth, num, free_branches

    def mutate(self, node):  # node value -> node of the same arity value
        index = self.nodes.index(node)
        valid_primitives = self.same_arity_primitives(self.nodes[index].arity)
        primitive = sample(valid_primitives, 1)[0]
        self.nodes[index].value = self.get_value(primitive)

    def same_arity_primitives(self, arity):  # return all primitives in the dictionary of given arity
        return [primitive for primitive in self.primitive_dict if primitive.get('arity') == arity]

    def same_arity_nodes(self, arity):  # this is invoked in headless chicken
        return [node for node in self.nodes if node.arity == arity]

    def stringify(self):  # tree to string export
        string = []
        for node in self.nodes:
            if not node.parent:
                string += ''.join(node.name + ',' + node.ptype + ',' + str(node.arity) + ',' + str(node.value) + '\n')
            else:
                string += ''.join(node.name + ',' + node.ptype + ',' + str(node.arity) + ',' + str(node.value) + ',' +
                                  node.parent.name + '\n')
        return ''.join(letter for letter in string)

    def parse(self, json):  # string to tree import
        importer = JsonImporter()

    def grow_leaf(self):
        valid_leafs = [primitive for primitive in self.primitive_dict if primitive.get('arity') == 0]
        leaf = valid_leafs[randint(0, len(valid_leafs) - 1)]
        value = self.get_value(leaf)
        return leaf.get('ptype'), value

    def grow_node(self, space_left):
        valid_nodes = [primitive for primitive in self.primitive_dict if primitive.get('arity') > 0]
        shuffle(valid_nodes)
        for node in valid_nodes:
            if not self.deadlock(space_left - node.get('arity')):
                value = self.get_value(node)
                return node.get('ptype'), node.get('arity'), value
        ptype, value = self.grow_leaf()
        return ptype, 0, value

    def deadlock(self, space_left):  # to identify deadlocks which might occur when size or depth of a tree is limited
        if space_left < 0:
            return True
        elif space_left == 0:
            return False
        for primitive in self.primitive_dict:
            arity = primitive.get('arity')
            if space_left - arity == 0 or \
                    space_left - arity == arity or \
                    space_left - arity > arity:
                return False
        return True

    def print(self):
        for pre, _, node in RenderTree(self.nodes[0]):
            print('%s%s' % (pre, node.value))

    def save_image(self, path):
        DotExporter(self.nodes[0], nodenamefunc=lambda node: '%s:%s' % (node.value, node.name)).to_picture(path)

    @staticmethod
    def get_value(primitive):
        if primitive.get('ptype') == 'bool':
            return randint(0, 1)
        elif primitive.get('ptype') == 'char':
            return sample(primitive.get('collection'), 1)[0]
        elif primitive.get('ptype') == 'real':
            return uniform(primitive.get('low'), primitive.get('up'))
        elif primitive.get('ptype') == 'int':
            return randint(primitive.get('low'), primitive.get('up'))
        elif primitive.get('ptype') == 'string':
            collection = primitive.get('collection')
            length = randint(1, primitive.get('length'))
            value = [sample(collection, 1)[0] for _ in range(length)]
            return ''.join(letter for letter in value)


if __name__ == '__main__':
    # 1-max
    dict_1 = [
        dict(ptype='bool', arity=1, collection=None, up=None, low=None),
        dict(ptype='bool', arity=0, collection=None, up=None, low=None)
    ]

    # TP1-max
    dict_2 = [
        dict(ptype='char', arity=0, collection=[1]),
        dict(ptype='char', arity=2, collection=['*', '+'])
    ]

    # ModGen
    dict_3 = [
        dict(ptype='char', arity=0, collection=['N']),
        dict(ptype='string', arity=0, collection=['C', 'D', '[', ']'], length=5),
        dict(ptype='string', arity=3, collection=['C', 'D', '[', ']'], length=5)
    ]

    max_size = 21
    max_depth = 10
    growth_constrain = False

    tree = Tree(max_size, max_depth, growth_constrain, dict_2)
    tree.grow()
    tree.print()
    tree.save_image('tp1_max.png')
    file = open('emigrant', 'w')
    file.write(tree.stringify())
