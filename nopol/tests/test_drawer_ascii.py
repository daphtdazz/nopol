import pytest
from pytest import param as prm

from nopol.drawers.ascii import ASCIIDrawer
from nopol.node import Node


def test_ascii_drawer_single_node():
    n1 = Node()
    drwr = ASCIIDrawer(n1)
    drwr.build()
    res = drwr.draw()
    assert res == """\
* Node 1
"""


@pytest.mark.parametrize('edges,result', [
    prm([
        ('Node 1', 'Node 2'),
        ('Node 1', 'Node 3'),
        ('Node 2', 'Node 4'),
        ('Node 2', 'Node 5'),
    ], r"""* Node 1
|\
| \
|  * Node 2
|  |\
|  | \
|  |  * Node 4
|  * Node 5
* Node 3""", id='simple-fan'),
    prm([
        ('Node 1', 'Node 2'),
        ('Node 1', 'Node 3'),
        ('Node 1', 'Node 6'),
        ('Node 2', 'Node 4'),
        ('Node 4', 'Node 7'),
        ('Node 2', 'Node 5'),
        ('Node 5', 'Node 8'),
        ('Node 5', 'Node 9'),
    ], r"""* Node 1
|\
| \
|  * Node 2
|  |\
|  | \
|  |  * Node 4
|  |  * Node 7
|  * Node 5
|  |\
|  | \
|  |  * Node 8
|  * Node 9
|\
| \
|  * Node 3
* Node 6""", id='various-splits-only'),
    prm([
        ('Node 1', 'Node 2'),
        ('Node 1', 'Node 3'),
        ('Node 2', 'Node 3'),
    ], r"""* Node 1
|\
| \
|  * Node 2
| /
|/
* Node 3""", id='simplest-merge'),
])
def test_ascii_drawer(edges, result):

    nodes = {}
    base_node = None
    for edge in edges:
        from_node_name, to_node_name = edge
        for name in (from_node_name, to_node_name):
            if name not in nodes:
                nodes[name] = Node(name)

        nodes[from_node_name].add_forward_node(nodes[to_node_name])
        if base_node is None:
            base_node = nodes[from_node_name]

    drwr = ASCIIDrawer(base_node)

    drwr.build()
    res = drwr.draw()

    assert res == result
