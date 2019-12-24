from enum import Enum


class Edge:
    DIRECTIONS = Enum('DIRECTIONS', ('forward', 'backward'))

    def __init__(self, backward_node, forward_node, direction=None):
        self.forward_node = forward_node
        self.backward_node = backward_node
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

    def __repr__(self):
        return f'{type(self).__name__}({self.backward_node}, {self.forward_node})'
