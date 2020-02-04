class Drawer:
    def __init__(self, node):
        self.base_node = node

    def build(self):
        raise NotImplementedError('Must implement build in a concrete subclass')

    def draw(self):
        raise NotImplementedError('Must implement draw in a concrete subclass')
