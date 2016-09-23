from unittest import TestCase

from src.fem.matrix_templates import SINGLE_LOCAL_MATRIX_POWERS_IN_DENOMINATOR as powers
from src.fem.matrix_templates import SINGLE_LOCAL_MATRIX_MULTIPLIERS as multipliers
from src.fem.fem import FEM
from src.fem.matrix_ops import MatrixOperations as Ops
from src.fem.matrix_ops import Matrix
from src.models.node import Node
from src.models.section import Section
from src.models.material import Material
from src.models.beam import Beam


class TestFEM(TestCase):
    def setUp(self):
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