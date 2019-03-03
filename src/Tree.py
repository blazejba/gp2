#!/usr/bin/env python3

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from random import randint, sample, uniform, random


class Tree:
    def __init__(self, size, depth, primitives):
        if size == 0 and depth == 0:
            self.unconstrained = True
        else:
            self.unconstrained = False
        self.max_size = size if size != 0 else 999
        self.max_depth = depth if depth != 0 else 99
        self.primitive_dict = primitives
        self.nodes = []

    def grow(self):  # first grow all the nodes then fill the remaining branches with leafs
        size, depth, num = [0] * 3
        free_branches = []

        # Growing nodes
        while True:
            size, depth, num, free_branches = self.expand(size, depth, num, free_branches)
            if size >= self.max_size or depth >= self.max_depth and not self.unconstrained:
                break
            elif self.unconstrained and len(free_branches) == 0:
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
        if num == 0 or (self.unconstrained and random() > 0.2):
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

    def stringify(self, how):  # tree to string export
        if how == 'soft':  # soft exports only the values
            return ''.join(letter for letter in [str(node.value) for node in self.nodes])
        elif how == 'hard':  # hard exports values, arities and primitive types
            string = []
            for index, node in enumerate(self.nodes):
                string += ''.join(node.ptype[0] + '(' + str(node.value) + ',' + str(node.arity) + ')')
                if index < len(self.nodes) - 1:
                    string += ''.join(',')
            return ''.join(letter for letter in string)

    def parse(self):  # string to tree import
        pass

    def grow_leaf(self):
        valid_leafs = [primitive for primitive in self.primitive_dict if primitive.get('arity') == 0]
        leaf = valid_leafs[randint(0, len(valid_leafs) - 1)]
        value = self.get_value(leaf)
        return leaf.get('ptype'), value

    def grow_node(self, space_left):
        valid_nodes = [primitive for primitive in self.primitive_dict if primitive.get('arity') > 0]
        while True:
            node = valid_nodes[randint(0, len(valid_nodes) - 1)]
            if not self.deadlock(space_left - node.get('arity')):
                break
        value = self.get_value(node)
        return node.get('ptype'), node.get('arity'), value

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


def nodenamefunc(node):
    return '%s:%s' % (node.value, node.name)


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

    max_size = 0
    max_depth = 4

    tree = Tree(max_size, max_depth, dict_1)
    tree.grow()
    print(RenderTree(tree.nodes[0]))
    DotExporter(tree.nodes[0], nodenamefunc=nodenamefunc).to_picture("tp1_max.png")
    print(tree.stringify('hard'))

    parsing = 's(C][,3),s(]D,3),s(]D,3),s(]DDC,3),s(C],3),s(C,0),c(N,0),s(CCDCD,0),s(CC]D,0),c(N,0),c(N,0),s(]DDC,0),s(C],0),s(D]D[C,0),s(D]C],0),c(N,0)'


