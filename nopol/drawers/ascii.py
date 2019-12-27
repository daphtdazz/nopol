from collections import namedtuple
from enum import Enum

from ..drawer import Drawer
from ..edge import Edge


class Line:
    def __init__(self, correlator):
        self.correlator = correlator


class ASCIILineDrawer:
    OPS = Enum('OPS', (
        'add_line', 'print_node', 'split_line',
        'swap_correlator', 'terminate_line'
    ))

    def __init__(self):
        self.ops = []
        # { line_corr: (line_index, line) }
        self.lines = {}
        self.ordered_lines = []

        # stores the results of drawing, which may be done by any operation
        self.output_lines = []

    def get_line(self, line_corr):
        return self.lines[line_corr][1]

    def add_line(self, line_corr, index='end'):
        # import pdb
        # pdb.set_trace()
        if index == 'end':
            line = Line(line_corr)
            self.lines[line_corr] = (len(self.ordered_lines), line)
            self.ordered_lines.append(line)
        else:
            line = Line(line_corr)
            line_tuple = (index, line)
            self.lines[line_corr] = line_tuple
            self.ordered_lines.insert(index, line)
            for later_line in self.ordered_lines[index + 1:]:
                old_index, line = self.lines[later_line.correlator]
                self.lines[later_line.correlator] = (old_index + 1, line)

    def add_op(self, op_name, *args):
        self.ops.append((op_name, args))

    def run(self):
        return
        for op in self.ops:
            self.perform_op(op[0], op[1])

    def draw(self):
        return '\n'.join(self.output_lines)

    def perform_op(self, op, *args):
        # import pdb
        # pdb.set_trace()
        self.add_op(op, *args)
        meth = getattr(self, f'op_{op.name}')
        meth(*args)

    def op_add_line(self, line_corr):
        self.add_line(line_corr)

    def op_print_node(self, line_corr, node):
        node_index, _ = self.lines[line_corr]
        num_lines = len(self.lines)
        self.output_lines.append(
            ' '.join([
                '  '.join([
                    *(['|'] * node_index),
                    '*',
                    *(['|'] * (num_lines - node_index - 1)),
                ]),
                node.description(),
            ])
        )

    def op_split_line(self, line_corr, new_corr):
        line_ind, line = self.lines[line_corr]
        new_line_ind = line_ind + 1

        line0_bits = []
        line0_bits.append('  '.join(['|'] * new_line_ind))
        line0_bits.append('\\')
        if new_line_ind < len(self.lines):
            line0_bits.append(' ')
            line0_bits.append('  '.join(['|'] * (len(self.lines) - line_ind)))

        self.output_lines.append(''.join(line0_bits))

        line1_bits = []
        line1_bits.append('  '.join(['|'] * new_line_ind))
        line1_bits.append(' \\')
        if new_line_ind < len(self.lines):
            line1_bits.append('  '.join(['|'] * (len(self.lines) - line_ind)))

        self.output_lines.append(''.join(line1_bits))

        self.add_line(new_corr, line_ind)

    def op_swap_correlator(self, old_corr, new_corr):
        (index, line) = self.lines.pop(old_corr)
        line.correlator = new_corr
        self.lines[new_corr] = (index, line)

    def op_terminate_line(self, corr):
        (ind, _) = self.lines.pop(corr)
        del self.ordered_lines[ind]


OPS = ASCIILineDrawer.OPS


class ASCIIDrawer(Drawer):

    def __init__(self, node, edges=None):
        super().__init__(node)
        self.line_drawer = ASCIILineDrawer()

    def ascii_node_info(self, layer):
        return layer.node.name

    def build(self):
        node = self.base_node

        first_corr = node if len(node.forward_edges) == 0 else node.forward_edges[0]
        self.line_drawer.perform_op(OPS.add_line, first_corr)
        self.update_line_drawer_from_node(node, first_corr)

    def update_line_drawer_from_node(self, node, on_corr):
        # self.line_drawer.perform_op(OPS.add_line, first_corr)
        self.line_drawer.perform_op(OPS.print_node, on_corr, node)

        if len(node.forward_edges) == 0:
            # no forward edges, so terminate the line
            self.line_drawer.perform_op(OPS.terminate_line, on_corr)
            return

        first_forward_edge = node.forward_edges[0]
        self.line_drawer.perform_op(
            OPS.swap_correlator, on_corr, first_forward_edge
        )
        if len(node.forward_edges) == 1:
            # one forward edge, print the subtree
            self.update_line_drawer_from_node(
                first_forward_edge.forward_node, first_forward_edge
            )
            # self.line_drawer.perform_op(
            #     OPS.print_node, first_forward_edge, first_forward_edge.forward_node
            # )
            # RECURSE
            return

        # self.line_drawer.swap_correlator(node, first_forward_edge)
        curr_edge = first_forward_edge
        for next_edge in node.forward_edges[1:]:
            self.line_drawer.perform_op(
                OPS.split_line, curr_edge, next_edge
            )
            self.update_line_drawer_from_node(curr_edge.forward_node, curr_edge)
            curr_edge = next_edge

        assert curr_edge is next_edge
        self.update_line_drawer_from_node(next_edge.forward_node, next_edge)

    def draw(self):
        return self.line_drawer.draw()
