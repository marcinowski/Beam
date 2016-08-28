from unittest import TestCase, main
from src.console_gui.console import ConsolePrintOut
from src.models.node import Node
from src.models.material import Material
from src.models.section import Section
from src.models.beam import Beam


class TestConsoleMode(TestCase):
    def test_node_print(self):
        Node.get_or_create(x=1, y=2)
        Node.get_or_create(x=2, y=3)
        Node.get_or_create(x=3, y=5)
        ConsolePrintOut().print_model(Node)

    def test_material_print(self):
        Material.get_or_create(name='long_long_name', young=13000, poisson=0.1)
        Material.get_or_create(name='s', young=123123, poisson=0.13)
        Material.get_or_create(name='name_3', young=123123, poisson=0.13)
        Material.get_or_create(name='name_4', young=123123, poisson=0.13)
        Material.get_or_create(name='name_5', young=123123, poisson=0.13)
        ConsolePrintOut().print_model(Material)

    def test_section_print(self):
        Section.get_or_create(name='test_1', area=0, inertia=13.12312)
        ConsolePrintOut().print_model(Section)

    def test_beam_print(self):
        Beam(
            start_node=Node.get_or_create(x=3, y=5),
            end_node=Node.get_or_create(x=1, y=2),
            material=Material.get_or_create(name='name_5', young=123123, poisson=0.13),
            section=Section.get_or_create(name='test_1', area=0, inertia=13.12312)
        )
        Beam(
            start_node=Node.get_or_create(x=1, y=2),
            end_node=Node.get_or_create(x=3, y=-1),
            material=Material.get_or_create(name='name_5', young=123123, poisson=0.13),
            section=Section.get_or_create(name='test_1', area=0, inertia=13.12312)
        )
        ConsolePrintOut().print_model(Beam)

if __name__ == '__main__':
    main()
