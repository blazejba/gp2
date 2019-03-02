#!/usr/bin/env python3

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from random import randint, sample, uniform, random


class Tree:
    def __init__(self, size, depth, primitives):
        self.max_size = size if size != 0 else 999
        self.max_depth = depth if depth != 0 else 99
        self.primitive_dict = primitives
        self.nodes = []

    def grow(self):
        size, depth, num = [0] * 3
        free_nodes = []

        # Growing nodes
        while True:
            size, depth, num, free_nodes = self.expand(size, depth, num, free_nodes)
            if size >= self.max_size or depth >= self.max_depth:
                break

        # Growing leafs
        while 0 < len(free_nodes):
            num, free_nodes = self.grow_leafs(num, free_nodes)

    def grow_leafs(self, num, free_nodes):
        ptype, value = self.select_leaf()
        parent = free_nodes[randint(0, len(free_nodes) - 1)]
        self.nodes.append(Node(str(num), ptype=ptype, arity=0, value=value, parent=parent))
        free_nodes.remove(parent)
        num += 1
        return num, free_nodes

    def expand(self, size, depth, num, free_nodes):
        space_left = self.max_size - size
        ptype, arity, value = self.select_node(space_left)
        if num == 0:
            self.nodes.append(Node(str(num), ptype=ptype, arity=arity, value=value))
        else:
            parent = free_nodes[randint(0, len(free_nodes) - 1)]
            self.nodes.append(Node(str(num), ptype=ptype, arity=arity, value=value, parent=parent))
            free_nodes.remove(parent)
        free_nodes += [self.nodes[-1]] * arity
        size += arity + 1 if num == 0 else arity
        depth = depth if self.nodes[-1].depth < depth else self.nodes[-1].depth + 1
        num += 1
        return size, depth, num, free_nodes

    def crossover(self):
        pass

    def point_mutation(self, mutation_rate):
        for node in self.nodes:
            if random() * 100 < mutation_rate:


    def headless_chicken_mutation(self):
        pass

    def stringify(self):
        pass

    def parse(self):
        pass

    def select_leaf(self):
        valid_leafs = [primitive for primitive in self.primitive_dict if primitive.get('arity') == 0]
        leaf = valid_leafs[randint(0, len(valid_leafs) - 1)]
        value = self.get_value(leaf)
        return leaf.get('name'), value

    def select_node(self, space_left):
        valid_nodes = [primitive for primitive in self.primitive_dict if primitive.get('arity') > 0]
        while True:
            node = valid_nodes[randint(0, len(valid_nodes) - 1)]
            if not self.deadlock(space_left - node.get('arity')):
                break
        value = self.get_value(node)
        return node.get('name'), node.get('arity'), value

    def deadlock(self, space_left):
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

    def get_value(self, primitive):
        if primitive.get('name') == 'Bool':
            return randint(0, 1)
        elif primitive.get('name') == 'Char':
            return sample(primitive.get('collection'), 1)[0]
        elif primitive.get('name') == 'Real':
            return uniform(primitive.get('low'), primitive.get('up'))
        elif primitive.get('name') == 'Int':
            return randint(primitive.get('low'), primitive.get('up'))
        elif primitive.get('name') == 'String':
            collection = primitive.get('collection')
            length = randint(0, primitive.get('length'))
            value = [sample(collection, 1)[0] for _ in range(length)]
            return ''.join(letter for letter in value)

def nodenamefunc(node):
    return '%s:%s' % (node.value, node.name)


if __name__ == '__main__':
    # 1-max
    dict_1 = [
        dict(name='Bool', arity=1, collection=None, up=None, low=None),
        dict(name='Bool', arity=0, collection=None, up=None, low=None)
    ]

    # TP1-max
    dict_2 = [
        dict(name='Char', arity=0, collection=[1]),
        dict(name='Char', arity=2, collection=['*', '+'])
    ]

    # ModGen
    dict_3 = [
        dict(name='Char', arity=0, collection=['None']),
        dict(name='String', arity=0, collection=['C', 'D', '[', ']'], length=5),
        dict(name='String', arity=3, collection=['C', 'D', '[', ']'], length=5)
    ]

    max_size = 0
    max_depth = 4

    tree = Tree(max_size, max_depth, dict_3)
    tree.grow()
    print(RenderTree(tree.nodes[0]))
    DotExporter(tree.nodes[0], nodenamefunc=nodenamefunc).to_picture("tp1_max.png")

