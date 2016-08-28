import sys
from unittest import TestCase, main

sys.path.append('D:\\Documents\\Programowanie\\Python\\Beam')
from src.models.node import Node
from src.models.meta import ObjectExists


class TestNodes(TestCase):
    def setUp(self):
        pass

    def test_node_uniqueness(self):
        Node(x=1, y=2)
        with self.assertRaises(ObjectExists):
            Node(x=1, y=2)

    def test_get_multiple(self):
        Node(x=3, y=2)
        Node(x=2, y=2)
        Node(x=3, y=3)
        self.assertEqual(len(Node.get_multiple(x=3)), 2)

    def test_get_or_create(self):
        Node(x=4, y=5)
        number_of_nodes = len(Node.objects)
        Node.get_or_create(x=4, y=5)
        self.assertEqual(number_of_nodes, len(Node.objects))
        Node.get_or_create(x=5, y=5)
        self.assertEqual(number_of_nodes+1, len(Node.objects))

    def test_sorting_ids(self):
        node = Node(x=6, y=6)
        test_id = node._id
        node_2 = Node(x=7, y=7)
        Node.remove(node)
        self.assertEqual(node_2._id, test_id)

    def test_deleting(self):
        node = Node(x=7, y=8)
        number_of_nodes = len(Node.objects)
        Node.remove(node)
        self.assertEqual(len(Node.objects), number_of_nodes-1)

if __name__ == "__main__":
    main()
