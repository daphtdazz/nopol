import pytest

from nopol.node import Node


@pytest.fixture(autouse=True)
def reset_node_counter():
    Node.counter = 1
