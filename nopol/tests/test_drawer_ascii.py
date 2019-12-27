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


def test_ascii_drawer():
    n1 = Node()
    n2 = Node()
    n3 = Node()
    n4 = Node()
    n5 = Node()

    n1.add_forward_node(n2)
    n1.add_forward_node(n3)
    n2.add_forward_node(n4)
    n2.add_forward_node(n5)

    drwr = ASCIIDrawer(n1)

    drwr.build()
    res = drwr.draw()

    assert res == r"""* Node 1
|\
| \
|  * Node 2
|  |\
|  | \
|  |  * Node 4
|  * Node 5
* Node 3"""
"""
   *
  /|\
 / | \
|  |\ \
|  | \
|  |\
|  | \
|  |  \
|  |  |\
|  |  | \
|  |  |  |
 \/   |  |
 /\   |  |
*  |  |  |
 \/_ /   |
 /  /\   |
|  |  |  |
 \__\/__/
 /\_  _/\
|   \/   |
|   /\   |
|  |  |  |
"""
