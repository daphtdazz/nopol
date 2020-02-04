from enum import Enum

from .utils import ParamReprMixin


class Edge(ParamReprMixin):
    DIRECTIONS = Enum('DIRECTIONS', ('forward', 'backward'))

    def __init__(self, backward_node, forward_node, direction=None):
        self.backward_node = backward_node
        self.forward_node = forward_node
        self.direction = None

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False

        return (
            self.direction,
            self.forward_node,
            self.backward_node
        ) == (
            other.direction,
            other.forward_node,
            other.backward_node
        )

    def __hash__(self):
        return id(self)

    def __str__(self):
        return f'{self.backward_node.name}--{self.forward_node.name}'
