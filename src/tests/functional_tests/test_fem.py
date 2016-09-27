from unittest import TestCase

from src.fem.matrix_templates import LOCAL_MATRIX_LENGTH_POWERS as powers
from src.fem.matrix_templates import LOCAL_MATRIX_MULTIPLIERS as multipliers
from src.fem.fem import FEM
from src.fem.matrix_ops import MatrixOperations as Ops
from src.models.node import Node
from src.models.section import Section
from src.models.material import Material
from src.models.beam import Beam
from src.models.load import Force
from src.models.supports import Support
from src.models.settings import Settings


class TestTemplate(TestCase):
    @staticmethod
    def start():
        Node.remove_all()
        Beam.remove_all()
        Force.remove_all()
        Support.remove_all()
        Section.remove_all()
        Material.remove_all()
        Settings.get_or_create()


class TestFEMBasic(TestTemplate):
    def setUp(self):
        self.start()
        self.beam = Beam.get_or_create(
            start_node=Node.get_or_create(x=0, y=0),
            end_node=Node.get_or_create(x=4, y=0),
            section=Section.get_or_create(name='', area=12, inertia=10),
            material=Material.get_or_create(name='', young=10, poisson=0.2)
        )
        self.fem = FEM()

    def test_matrix_templates(self):
        self.assertEqual(multipliers, Ops().transpose(multipliers))
        self.assertEqual(powers, Ops().transpose(powers))

    def test_local_single_k_matrix(self):
        k_matrix = self.fem._generate_single_local_stiffness_matrix(self.beam)
        self.assertEqual(k_matrix, Ops().transpose(k_matrix))

    def test_generating_global_K(self):
        self.fem.generate_global_stiffness_matrix()
        self.assertEqual(self.fem.global_k, Ops().transpose(self.fem.global_k))


class TestFEMComplex(TestTemplate):
    def setUp(self):
        self.start()
        Beam.get_or_create(
            start_node=Node.get_or_create(x=0, y=0),
            end_node=Node.get_or_create(x=4, y=0),
            section=Section.get_or_create(name='', area=12, inertia=10),
            material=Material.get_or_create(name='', young=10, poisson=0.2)
        )
        Beam.get_or_create(
            start_node=Node.get_or_create(x=4, y=0),
            end_node=Node.get_or_create(x=4, y=4),
            section=Section.get_or_create(name='', area=12, inertia=10),
            material=Material.get_or_create(name='', young=10, poisson=0.2)
        )
        self.fem = FEM()

    def test_generating_global_K(self):
        self.fem.generate_global_stiffness_matrix()
