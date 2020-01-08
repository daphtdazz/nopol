from collections.abc import Callable, Iterable
from enum import Enum
from itertools import zip_longest

from nopol.node import Node


RED_CCHAR = '\x1b[31m'
RESET_CCHAR = '\x1b[0m'


class InvalidDrawing(Exception):
    pass


class HLine:
    # ----------------------------------------------------------------------------------------------
    # Public Methods
    # ----------------------------------------------------------------------------------------------
    def __init__(self):
        self.vlines = []
        self.arriving_vlines = []
        self.departing_vlines = []
        self.node = None
        self.node_vline = None

    def add_vline(self, vline=None):
        vline = self._curr_or_new_vline(vline)
        self.vlines.append(vline)
        return vline

    def add_departing_vline(self, from_vline, vline=None):
        vline = self._curr_or_new_vline(vline)
        vline.start_h_v_lines = (self, from_vline)
        self.departing_vlines.append(vline)
        return vline

    def add_arriving_vline(self, to_vline, vline):
        vline.end_h_v_lines = (self, to_vline)
        self.arriving_vlines.append(vline)

        try:
            curr_index = self.vlines.index(vline)
        except ValueError:
            # not a current line
            return

        del self.vlines[curr_index]

    def put_node(self, vline, node):
        self.node = node
        assert vline in self.vlines
        self.node_vline = vline

    # ----------------------------------------------------------------------------------------------
    # Methods for friends
    # ----------------------------------------------------------------------------------------------
    def propagate(self):
        hl = HLine()
        hl.vlines = list(self.vlines)
        for dvl in self.departing_vlines:
            from_vl = dvl.start_h_v_lines[1]
            from_index = hl.vlines.index(from_vl)
            hl.vlines[from_index + 1:from_index + 1] = [dvl]
        return hl

    def index_of_vline(self, vline):
        try:
            return self.vlines.index(vline)
        except ValueError:
            pass

        if vline.start_h_v_lines is not None:
            shl, svl = vline.start_h_v_lines
            if shl is self:
                return self.vlines.index(svl)

        if vline.end_h_v_lines is not None:
            ehl, evl = vline.end_h_v_lines
            if ehl is self:
                return self.vlines.index(evl)

        raise InvalidDrawing(f'{vline} does not commence, terminate or passthrough {self}')

    # ----------------------------------------------------------------------------------------------
    # Internal
    # ----------------------------------------------------------------------------------------------
    def _curr_or_new_vline(self, vline):
        if vline is None:
            return VLine()
        return vline


class VLine:
    def __init__(
        self, correlator=None
    ):
        self.correlator = correlator
        self.start_h_v_lines = None
        self.end_h_v_lines = None

    def __hash__(self):
        return id(self)


def list_join(join: list, itr: Iterable):
    res = []
    for ind, obj in enumerate(itr):
        if ind > 0:
            res.extend(join)
        res.append(obj)
    return res


def list_rstrip_in_place(alist: list, func: Callable):
    while len(alist) > 0:
        if func(alist[-1]):
            alist.pop()
            continue
        break


def list_rstrip(alist: list, func: Callable):
    rlist = list(alist)
    list_rstrip_in_place(rlist, func)
    return rlist


def line_is_just_passthrough(line):
    return all(char in [' ', '|'] for char in line)


class ASCIILineDrawer:
    # ----------------------------------------------------------------------------------------------
    # Public Methods
    # ----------------------------------------------------------------------------------------------
    def __init__(self):
        self.hlines = []
        self.canvas = []

    def draw(self):
        self._draw_to_canvas()
        return ''.join(''.join(list_rstrip(line, lambda c: c == ' ')) + '\n' for line in self.canvas)

    def add_hline(self):
        if len(self.hlines) == 0:
            hl = HLine()
        else:
            hl = self.hlines[-1].propagate()
        self.hlines.append(hl)
        return hl

    # ----------------------------------------------------------------------------------------------
    # Extension points for subclasses (??)
    # ----------------------------------------------------------------------------------------------
    def optimize_canvas(self):
        self.canvas = [
            line
            for line in self.canvas
            if not line_is_just_passthrough(line)
        ]

    # ----------------------------------------------------------------------------------------------
    # Internal
    # ----------------------------------------------------------------------------------------------
    def _draw_to_canvas(self):
        max_vlines = max(len(hl.vlines) for hl in self.hlines)

        # reset the canvas
        self.canvas = [
            list_join([' ', ' '], [' '] * max_vlines)
            for _ in range(len(self.hlines) * 3 - 2)
        ]

        for ind, hline in enumerate(self.hlines):
            if ind > 0:
                self._draw_join(ind - 1)

            self._draw_hline(ind)

        self.optimize_canvas()

    def _draw_hline(self, index):
        hline = self.hlines[index]
        canvas_line = self._canvas_line_for_hline_ind(index)
        for vl_ind, vl in enumerate(hline.vlines):
            canvas_line_ind = vl_ind * 3
            if vl == hline.node_vline:
                canvas_line[canvas_line_ind] = '*'
            else:
                canvas_line[canvas_line_ind] = '|'

        list_rstrip_in_place(canvas_line, lambda x: x == ' ')

        if hline.node is not None:
            canvas_line.extend([' ', str(hline.node.name)])

    def _draw_join(self, index):
        hline_above = self.hlines[index]
        hline_below = self.hlines[index + 1]

        hline_draw_ind = index * 3

        for vl_start_ind, vl in (
            (ind, vl)
            for itr in [
                enumerate(hline_above.vlines),
                (
                    (hline_above.index_of_vline(vl), vl)
                    for vl in hline_above.departing_vlines
                )
            ]
            for ind, vl in itr
        ):
            ind_below = hline_below.index_of_vline(vl)
            if ind_below == vl_start_ind:
                self._draw_chars([
                    (hline_draw_ind + 1, vl_start_ind * 3, '|'),
                    (hline_draw_ind + 2, vl_start_ind * 3, '|'),
                ], 'straight_line')
                continue

            if abs(ind_below - vl_start_ind) > 1:
                raise InvalidDrawing(f'{vl} changes position by more than 1 after {hline_above}')

            if ind_below > vl_start_ind:
                self._draw_chars([
                    (hline_draw_ind + 1, vl_start_ind * 3 + 1, '\\'),
                    (hline_draw_ind + 2, vl_start_ind * 3 + 2, '\\'),
                ], 'right_slant')
                continue

            if ind_below < vl_start_ind:
                self._draw_chars([
                    (hline_draw_ind + 1, vl_start_ind * 3 - 1, '/'),
                    (hline_draw_ind + 2, vl_start_ind * 3 - 2, '/'),
                ], 'left_slant')
                continue

            raise RuntimeError('Logic error')

    def _canvas_line_for_hline_ind(self, hline_ind):
        return self.canvas[hline_ind * 3]

    def _draw_chars(self, coord_char_tuples, line_name):
        for hind, vind, char in coord_char_tuples:
            if self.canvas[hind][vind] != ' ':
                raise InvalidDrawing(
                    f'{line_name} cuts something at {hind},{vind}: {self.canvas}'
                )
            self.canvas[hind][vind] = char
