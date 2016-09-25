from unittest import TestCase

from src.fem.matrix_templates import LOCAL_MATRIX_LENGTH_POWERS as powers
from src.fem.matrix_templates import LOCAL_MATRIX_MULTIPLIERS as multipliers
from src.fem.fem import FEM
from src.fem.matrix_ops import MatrixOperations as Ops
from src.fem.matrix_ops import Matrix
from src.models.node import Node
from src.models.section import Section
from src.models.material import Material
from src.models.beam import Beam
from src.models.settings import Settings


class TestFEMBasic(TestCase):
    def setUp(self):
        Beam.remove_all()
        Settings.get_or_create()
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
        for i in k_matrix:
            print(i)
        self.assertEqual(k_matrix, Ops().transpose(k_matrix))

    def test_generating_global_K(self):
        K_global = self.fem.generate_global_stiffness_matrix()
        for i in K_global:
            print(i)
        print('_____________________')
        self.assertEqual(K_global, Ops().transpose(K_global))


class TestFEMComplex(TestCase):
    def setUp(self):
        Beam.remove_all()
        Settings.get_or_create()
        self.beam = Beam.get_or_create(
            start_node=Node.get_or_create(x=0, y=0),
            end_node=Node.get_or_create(x=4, y=0),
            section=Section.get_or_create(name='', area=12, inertia=10),
            material=Material.get_or_create(name='', young=10, poisson=0.2)
        )
        self.beam = Beam.get_or_create(
            start_node=Node.get_or_create(x=4, y=0),
            end_node=Node.get_or_create(x=4, y=4),
            section=Section.get_or_create(name='', area=12, inertia=10),
            material=Material.get_or_create(name='', young=10, poisson=0.2)
        )
        self.fem = FEM()

    def test_generating_global_K(self):
        k_global = self.fem.generate_global_stiffness_matrix()
        for i in k_global:
            print(i)
