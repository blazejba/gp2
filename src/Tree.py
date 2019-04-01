#!/usr/bin/env python3

from numpy import zeros
from scipy.cluster.vq import kmeans, vq, whiten

from anytree import Node, RenderTree, findall_by_attr, PreOrderIter
from anytree.exporter import DotExporter
from random import randint, sample, uniform, shuffle, random
from copy import deepcopy


class Tree:
    def __init__(self, size, depth, primitives, full):
        self.full = full    # grow all branches to max depth
        self.max_size = size if size != 0 else 999
        self.max_depth = depth if depth != 0 else 999
        self.primitive_dict = primitives
        self.nodes = []

    def grow(self):  # first grow all the nodes then fill the remaining branches with leafs
        size, depth = 0, 0
        free_branches = []

        # Growing nodes
        if self.full:
            # grow root
            ptype, arity, value = self.primitive_root()
            self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=arity, value=value))
            free_branches += [self.nodes[-1]] * arity
            while len(free_branches) > 0:
                current_depth = free_branches[0].depth
                parent = free_branches[0]
                if current_depth < self.max_depth - 1:
                    ptype, arity, value = self.primitive_function(self.max_size)
                    self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=arity, value=value, parent=parent))
                else:
                    ptype, value = self.primitive_terminal()
                    arity = 0
                    self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=arity, value=value, parent=parent))
                free_branches += [self.nodes[-1]] * arity
                free_branches.remove(parent)
            return
        else:
            while True:
                size, depth, free_branches = self.grow_function(size, depth, free_branches)
                if size >= self.max_size or depth >= self.max_depth or len(free_branches) == 0:
                    break

        # Growing leafs
        while 0 < len(free_branches):
            free_branches = self.grow_leaf(free_branches)

    def grow_leaf(self, free_branches):  # grow a random terminal node
        ptype, value = self.primitive_terminal()
        parent = free_branches[randint(0, len(free_branches) - 1)]
        self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=0, value=value, parent=parent))
        free_branches.remove(parent)
        return free_branches

    def grow_function(self, size, depth, free_branches):  # expand tree by growing a new function node
        space_left = self.max_size - size
        if depth == 0:
            ptype, arity, value = self.primitive_root()
            self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=arity, value=value))
        else:
            ptype, arity, value = self.primitive_function(space_left)
            if self.full:
                parent = free_branches[0]
            else:
                parent = free_branches[randint(0, len(free_branches) - 1)]
            self.nodes.append(Node(self.generate_name(), ptype=ptype, arity=arity, value=value, parent=parent))
            free_branches.remove(parent)
        free_branches += [self.nodes[-1]] * arity
        size += arity + 1 if depth == 0 else arity
        depth = depth if self.nodes[-1].depth < depth else self.nodes[-1].depth + 1
        return size, depth, free_branches

    def primitive_root(self):
        for primitive in self.primitive_dict:
            if primitive.get('ptype') == 'root':
                return 'root', primitive.get('arity'), '#'
        return self.primitive_function(self.max_size)

    def primitive_terminal(self):
        valid_leafs = [primitive for primitive in self.primitive_dict if primitive.get('arity') == 0]
        leaf = valid_leafs[randint(0, len(valid_leafs) - 1)]
        value = self.get_new_value(leaf)
        return leaf.get('ptype'), value

    def primitive_function(self, space_left):
        valid_nodes = [primitive for primitive in self.primitive_dict if primitive.get('arity') > 0 and primitive.get('ptype') != 'root']
        shuffle(valid_nodes)
        for node in valid_nodes:
            if not self.deadlock(space_left - node.get('arity')):
                value = self.get_new_value(node)
                return node.get('ptype'), node.get('arity'), value

        # if no valid function has been found, grow a terminal instead
        ptype, value = self.primitive_terminal()
        return ptype, 0, value

    def generate_name(self):
        return str(len(self.nodes))

    # currently doesnt work
    def headless_chicken(self):     # alternative mutation, a random node is attached to a freshly generated branch
        if len(self.nodes) == self.max_size or self.full:
            self.nodes = []
            self.grow()
            return
        while True:
            cutoff_node = self.nodes[randint(0, len(self.nodes) - 1)]   # select random node where new branch will be
            if cutoff_node.parent:
                break
        branch, free_node, _ = self.detach_branch(cutoff_node)   # cut off the branch and keep the free node
        del branch  # branch can be discarded because the purpose of headless chicken is to grow a new one
        free_branches = [free_node]
        self.rename(0)

        # find depth of tree
        depth = 0
        for node in self.nodes:
            if node.depth > depth:
                depth = node.depth

        while True:     # 90% grow function nodes, 10% terminal nodes
            if random() > 0.5 and self.max_depth > depth:
                _, depth, free_branches = self.grow_function(0, depth, free_branches)
            else:
                free_branches = self.grow_leaf(free_branches)
            if len(free_branches) == 0:  # do until max depth or no free nodes
                break

    def crossover(self, chromosome_a, chromosome_b):
        parent_a = deepcopy(chromosome_a)
        parent_b = deepcopy(chromosome_b)
        parent_a.rename(0)
        parent_b.rename(len(parent_a.nodes))
        valid_nodes_b, crossover_node_a, crossover_node_b = [], object, object

        # finding crossover points A and B
        while len(valid_nodes_b) == 0:
            random_choice = randint(1, len(parent_a.nodes) - 1)
            crossover_node_a = parent_a.nodes[random_choice]
            valid_nodes_b = parent_b.same_arity_nodes(crossover_node_a.arity)
            if len(parent_a.nodes) == self.max_size:
                valid_nodes_b = [node for node in valid_nodes_b
                                 if len(node.descendants) == len(crossover_node_a.descendants)]
        crossover_node_b = valid_nodes_b[randint(0, len(valid_nodes_b) - 1)]

        # detaching branches at crossover point
        branch_a, free_node_a, position_in_children_a = parent_a.detach_branch(crossover_node_a)
        branch_b, free_node_b, position_in_children_b = parent_b.detach_branch(crossover_node_b)

        # attaching branches
        parent_a.attach_branch(free_node_a, branch_b, position_in_children_a)
        parent_b.attach_branch(free_node_b, branch_a, position_in_children_b)

        # remove branches if max depth is exceeded
        #

        self.nodes = parent_a.nodes
        return parent_b

    def attach_branch(self, node, branch, index):
        children_list = list(node.children)
        children_list = children_list[:index] + [branch[0]] + children_list[index:]
        node.children = tuple(children_list)
        self.nodes += branch

    def detach_branch(self, detached_node):
        free_node = detached_node.parent
        position_in_children = free_node.children.index(detached_node)
        detached_node.parent = None
        if len(detached_node.descendants) > 0:
            branch = [detached_node] + list(detached_node.descendants)
        else:
            branch = [detached_node]
        self.nodes = [node for node in self.nodes if node not in branch]
        return branch, free_node, position_in_children

    def get_primitive(self, name, arity):
        for primitive in self.primitive_dict:
            if primitive.get('ptype') == name and primitive.get('arity') == arity:
                return primitive

    def same_arity_nodes(self, arity):  # this is invoked in headless chicken
        same_arity_nodes = findall_by_attr(self.nodes[0].root, value=arity, name='arity')
        return [node for node in same_arity_nodes if node.parent]  # same arity nodes minus root

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

    @staticmethod
    def get_new_value(primitive):
        if primitive.get('ptype') == 'bool':
            return randint(0, 1)
        elif primitive.get('ptype') == 'char':
            value = sample(primitive.get('collection'), 1)[0]
            return value
        elif primitive.get('ptype') == 'real':
            return uniform(primitive.get('low'), primitive.get('up'))
        elif primitive.get('ptype') == 'int':
            return randint(primitive.get('low'), primitive.get('up'))
        elif primitive.get('ptype') == 'string':
            collection = primitive.get('collection')
            length = randint(1, primitive.get('length'))
            value = sample(collection, length)
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
        dict(ptype='root', arity=9),
        dict(ptype='string', arity=0, collection=['C', 'X', 'Y', 'Z', '-', '+', '[', ']'], length=4)
    ]

    # Symbolic Regression
    dict_4 = [
        dict(ptype='char', arity=0, collection=['x']),
        dict(ptype='real', arity=0, up=4, low=-4),
        dict(ptype='char', arity=2, collection=['*', '+', '%', '^'])
    ]

    max_size = 0
    max_depth = 2
    unique = False

    forest = [Tree(max_size, max_depth, dict_3, unique)]
    forest[0].grow()
