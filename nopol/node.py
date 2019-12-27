from .descriptors import Singular
from .edge import Edge
from .utils import ParamReprMixin


class Node(ParamReprMixin):
    omitted_repr_params = set([
        'forward_edges', 'undirected_edges', 'backward_edges', 'info'
    ])

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

    def description(self):
        return self.name
