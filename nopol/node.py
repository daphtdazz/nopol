from .descriptors import Singular
from .edge import Edge


class Node:

    counter = 1

    @classmethod
    def next_name(cls):
        curr_counter = cls.counter
        cls.counter = curr_counter + 1
        return f'Node {curr_counter}'

    def __init__(self, name=None, **kwargs):
        self.name = name if name is not None else self.next_name()
        self.forward_edges = []
        self.undirected_edges = []
        self.backward_edges = []
        self.info = kwargs

    def add_forward_nodes(self, fnodes):
        for fnode in fnodes:
            edge = Edge(self, fnode)
            self.forward_edges.append(edge)

    add_forward_node = Singular(add_forward_nodes)

    def add_backward_nodes(self, bnodes):
        for bnode in bnodes:
            edge = Edge(bnode, self)
            self.backward_edges.append(edge)

    add_backward_node = Singular(add_backward_nodes)

    def __str__(self):
        return f'{type(self).__name__}(name={self.name!r})'
