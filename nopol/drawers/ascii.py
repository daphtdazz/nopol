from .ascii_line_drawer import ASCIILineDrawer
from ..drawer import Drawer

RED_CCHAR = '\x1b[31m'
RESET_CCHAR = '\x1b[0m'


class ASCIIDrawer(Drawer):
    def __init__(self, base_node):
        super().__init__(base_node)
        self.ascii_line_drawer = ASCIILineDrawer()

