from nopol.drawers.ascii import ASCIILineDrawer
from nopol.node import Node


def test_ascii_line_drawer_v3():
    drwr = ASCIILineDrawer()

    n1 = Node()

    h1 = drwr.add_hline()
    v1 = h1.add_vline()
    h1.put_node(v1, n1)
    assert drwr.draw() == """\
* Node 1
"""

    h2 = drwr.add_hline()
    n2 = Node()
    h2.put_node(v1, n2)
    assert drwr.draw() == """\
* Node 1
* Node 2
"""

    v2 = h2.add_departing_vline(v1)
    h3 = drwr.add_hline()
    n3 = Node()
    h3.put_node(v2, n3)

    v3 = h3.add_departing_vline(v2)
    h4 = drwr.add_hline()
    n4 = Node()
    h4.put_node(v3, n4)

    h5 = drwr.add_hline()
    n5 = Node()
    h5.put_node(v2, n5)

    h6 = drwr.add_hline()
    h6.add_arriving_vline(v2, v3)
    h6.put_node(v2, Node())

    v12 = h6.add_departing_vline(v1)
    v21 = h6.add_departing_vline(v2)
    h7 = drwr.add_hline()
    h7.add_arriving_vline(v2, v12)
    h7.add_arriving_vline(v1, v21)
    h7.put_node(v1, Node())

    h8 = drwr.add_hline()
    h8.add_arriving_vline(v2, v1)
    h8.put_node(v2, Node())

    assert drwr.draw() == r"""* Node 1
* Node 2
|\
| \
|  * Node 3
|  |\
|  | \
|  |  * Node 4
|  *  | Node 5
|  | /
|  |/
|  * Node 6
|\/|
|/\|
*  | Node 7
| /
|/
* Node 8
"""
