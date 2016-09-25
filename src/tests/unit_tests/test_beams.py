from unittest import TestCase, main, skip
from src.models.node import Node
from src.models.section import Section
from src.models.material import Material
from src.models.beam import Beam


class TestBeams(TestCase):
    def setUp(self):
        self.node_1 = Node.get_or_create(x=0, y=0)
        self.node_2 = Node.get_or_create(x=2, y=2)
        self.node_3 = Node.get_or_create(x=4, y=0)
        self.section = Section.get_or_create(name='test_section', area=10, inertia=100)
        self.material = Material.get_or_create(name='test_material', young=10000, poisson=0.4)
        self.beam_1 = Beam.get_or_create(
            start_node=self.node_1,
            end_node=self.node_2,
            section=self.section,
            material=self.material
        )
        self.beam_2 = Beam.get_or_create(
            start_node=self.node_1,
            end_node=self.node_3,
            section=self.section,
            material=self.material,
        )

    def test_is_beam_instance(self):
        self.assertIsInstance(self.beam_1, Beam)
        self.assertIsInstance(self.beam_2, Beam)

    def test_beams_params(self):
        self.assertEqual(self.beam_1.section.area, 10)
        self.assertEqual(self.beam_2.material.poisson, 0.4)

    def test_beam_length(self):
        self.assertEqual(4, self.beam_2.length())

if __name__ == '__main__':
    main()
