#!/usr/bin/env python3

from anytree import Node, RenderTree, findall_by_attr, PreOrderIter, find
from anytree.exporter import DotExporter
from random import randint, sample, uniform, shuffle, random
from copy import deepcopy


class Tree:
    def __init__(self, size, depth, constrained, primitives, unique):
        self.constrained = constrained
        if not constrained:
            self.max_size = randint(5, size)
            self.max_depth = randint(1, depth)
        else:
            self.max_size = size if size != 0 else 999
            self.max_depth = depth if depth != 0 else 999
        self.primitive_dict = primitives
        self.nodes = []
        self.unique = unique

    def grow(self):  # first grow all the nodes then fill the remaining branches with leafs
        size, depth = 0, 0
        free_branches = []

        # Growing nodes
        while True:
            size, depth, free_branches = self.grow_function(size, depth, free_branches)
            if size >= self.max_size or depth >= self.max_depth or len(free_branches) == 0:
                break

        # Growing leafs
        while 0 < len(free_branches):
            free_branches = self.grow_leaf(free_branches)

    def grow_leaf(self, free_branches):  # grow a random terminal node
        ptype, value = self.primitive('terminal')
        parent = free_branches[randint(0, len(free_branches) - 1)]
        self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=0, value=value, parent=parent))
        free_branches.remove(parent)
        return free_branches

    def grow_function(self, size, depth, free_branches):  # expand tree by growing a new function node
        space_left = self.max_size - size
        ptype, arity, value = self.primitive('function', space_left)
        if depth == 0:
            self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=arity, value=value))
        else:
            parent = free_branches[randint(0, len(free_branches) - 1)]
            self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=arity, value=value, parent=parent))
            free_branches.remove(parent)
        free_branches += [self.nodes[-1]] * arity
        size += arity + 1 if depth == 0 else arity
        depth = depth if self.nodes[-1].depth < depth else self.nodes[-1].depth + 1
        return size, depth, free_branches

    def primitive(self, which, space_left=None):
        if which == 'terminal':
            valid_leafs = [primitive for primitive in self.primitive_dict if primitive.get('arity') == 0]
            leaf = valid_leafs[randint(0, len(valid_leafs) - 1)]
            value = self.get_value(leaf)
            return leaf.get('ptype'), value
        else:
            valid_nodes = [primitive for primitive in self.primitive_dict if primitive.get('arity') > 0]
            shuffle(valid_nodes)
            for node in valid_nodes:
                if not self.deadlock(space_left - node.get('arity')):
                    value = self.get_value(node)
                    return node.get('ptype'), node.get('arity'), value
            ptype, value = self.primitive('terminal')
            return ptype, 0, value

    def generate_name(self):
        return str(len(self.nodes))

    def headless_chicken(self):     # alternative mutation, a random node is attached to a freshly generated branch
        cutoff_node = self.nodes[randint(1, len(self.nodes) - 1)]   # select random node where new branch will be
        branch, free_node = self.detach_branch(cutoff_node)     # cut off the branch and keep the free node
        del branch  # branch can be discarded because the purpose of headless chicken is to grow a new one
        free_branches = [free_node]
        self.rename(0)

        depth = 0
        for node in self.nodes:
            if node.depth > depth:
                depth = node.depth

        # the problem lies in here
        while True:     # 90% grow function nodes, 10% terminal nodes
            #print('here', 'max depth', self.max_depth, 'depth', depth, free_branches)
            if random() > 0.1 and not self.max_depth < depth:
                _, depth, free_branches = self.grow_function(0, depth, free_branches)
            else:
                free_branches = self.grow_leaf(free_branches)
            if len(free_branches) == 0:  # do until max depth or no free nodes
                break
        # end of where the problem lies

    def mutate(self, node):  # node value -> node of the same arity value
        index = self.nodes.index(node)
        valid_primitives = self.same_arity_primitives(self.nodes[index].arity)
        primitive = sample(valid_primitives, 1)[0]
        self.nodes[index].value = self.get_value(primitive)

    def crossover(self, parents):
        parent_a = deepcopy(parents[0])
        parent_b = deepcopy(parents[1])
        parent_a.rename(0)
        parent_b.rename(len(parent_a.nodes))

        valid_nodes_b, crossover_node_a, crossover_node_b = [], object, object

        # finding crossover point
        while len(valid_nodes_b) == 0:
            crossover_node_a = parent_a.nodes[randint(1, len(parent_a.nodes) - 1)]
            valid_nodes_b = parent_b.same_arity_nodes(crossover_node_a.arity)
            if self.constrained:
                valid_nodes_b = [node for node in valid_nodes_b
                                 if len(node.descendants) == len(crossover_node_a.descendants)]
        crossover_node_b = valid_nodes_b[randint(0, len(valid_nodes_b) - 1)]

        # detaching branches at crossover point
        branch_a, free_node_a = parent_a.detach_branch(crossover_node_a)
        branch_b, free_node_b = parent_b.detach_branch(crossover_node_b)

        # attaching branches
        parent_a.attach_branch(free_node_a, branch_b)
        parent_b.attach_branch(free_node_b, branch_a)

        # selecting one of the two trees
        self.nodes = parent_a.nodes
        return parent_b

    def attach_branch(self, node, branch):
        branch[0].parent = node
        self.nodes += branch

    def detach_branch(self, detaching_node):
        cutoff_node = find(self.nodes[0].root, lambda node: node.name == detaching_node.name)
        free_node = cutoff_node.parent
        cutoff_node.parent = None
        if len(cutoff_node.descendants) > 0:
            branch = [cutoff_node] + list(cutoff_node.descendants)
        else:
            branch = [cutoff_node]
        self.nodes = [node for node in self.nodes if node not in branch]
        return branch, free_node

    def same_arity_primitives(self, arity):  # return all primitives in the dictionary of given arity
        return [primitive for primitive in self.primitive_dict if primitive.get('arity') == arity]

    def same_arity_nodes(self, arity):  # this is invoked in headless chicken
        return findall_by_attr(self.nodes[0].root, value=arity, name='arity')

    def stringify(self):  # tree to string export
        string = []
        for index, node in enumerate(self.nodes):
            string += ''.join(node.name + ',' + node.ptype + ',' + str(node.arity) + ',' + str(node.value) + ',' +
                              (str(node.parent.name) if node.parent else ''))
            if index < len(self.nodes) - 1:
                string += '\n'
        return ''.join(letter for letter in string)

    def parse(self, text):  # string to tree import
        string_nodes = text.split('\n')
        for string_node in string_nodes:
            name, ptype, arity, value, parent = string_node.split(',')

            arity = int(arity)

            if not parent == '':  # finding
                for node in self.nodes:
                    if node.name == parent:
                        parent = node

            if ptype == 'bool' or ptype == 'int':
                value = int(value)
            if ptype == 'real':
                value = float(value)

            new_node = Node(name, ptype=ptype, arity=arity, value=value, parent=parent) if not parent == '' else \
                Node(name, ptype=ptype, arity=arity, value=value)
            self.nodes += [new_node]

    def deadlock(self, space_left):  # to identify deadlocks which might occur when size or depth of a tree are limited
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

    def tree_in_line(self):
        return ''.join(letter for letter in [str(node.value) + ' ' for node in PreOrderIter(self.nodes[0].root)])

    def save_image(self, path):
        DotExporter(self.nodes[0], nodenamefunc=lambda node: '%s:%s' % (node.value, node.name)).to_picture(path)

    def get_value(self, primitive):
        if primitive.get('ptype') == 'bool':
            return randint(0, 1)
        elif primitive.get('ptype') == 'char':
            return sample(primitive.get('collection'), 1)[0]
        elif primitive.get('ptype') == 'real':
            return uniform(primitive.get('low'), primitive.get('up'))
        elif primitive.get('ptype') == 'int':
            return randint(primitive.get('low'), primitive.get('up'))
        elif primitive.get('ptype') == 'string':
            while True:
                collection = primitive.get('collection')
                length = randint(1, primitive.get('length'))
                value = [sample(collection, 1)[0] for _ in range(length)]
                if value not in [node.value for node in self.nodes]:
                    break
            return ''.join(letter for letter in value)

    def rename(self, base):
        for num, node in enumerate(self.nodes):
            node.name = str(num + base)


class TreeReadOnly:
    def __init__(self, text):
        self.nodes = []
        self.parse(text)

    def parse(self, text):  # string to tree import
        nodes = []
        string_nodes = text.split('\n')
        for string_node in string_nodes:
            name, ptype, arity, value, parent = string_node.split(',')
            if parent != '':
                for node in nodes:
                    if node.name == parent:
                        parent = node
            nodes += [Node(name, ptype=ptype, arity=arity, value=value, parent=parent) if parent != ''
                      else Node(name, ptype=ptype, arity=arity, value=value)]
        self.nodes = nodes


if __name__ == '__main__':
    # 1-max
    dict_1 = [
        dict(ptype='bool', arity=1),
        dict(ptype='bool', arity=0)
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

    # Symbolic Regression
    dict_4 = [
        dict(ptype='char', arity=0, collection=['x']),
        dict(ptype='real', arity=0, up=4, low=-4),
        dict(ptype='char', arity=2, collection=['*', '+', '%', '^'])
    ]

    max_size = 15
    max_depth = 6
    constrained = True
    unique = False

    parent_a = Tree(max_size, max_depth, constrained, dict_4, unique)
    parent_a.grow()
    parent_a.print()
    parent_a.headless_chicken()
    parent_a.print()
