from nopol.edge import Edge
from nopol.node import Node


def test_node_simples():
    node1 = Node()
    node2 = Node()

    node1.add_forward_node(node2)
    assert node1.forward_edges == [Edge(node1, node2)]
