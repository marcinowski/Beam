from src.tests.functional_tests.test_fem import TestTemplate
from src.fem.fem import FEM
from src.fem.matrix_ops import MatrixOperations as Ops
from src.models.node import Node
from src.models.section import Section
from src.models.material import Material
from src.models.beam import Beam
from src.models.load import Force
from src.models.supports import Support
from src.fem.matrix_ops import Matrix


class TestFEMExample(TestTemplate):
    def setUp(self):
        self.start()
        Beam.get_or_create(
            start_node=Node.get_or_create(x=0, y=0),
            end_node=Node.get_or_create(x=4, y=3),
            section=Section.get_or_create(name='sect_1', area=0.02, inertia=0.001),
            material=Material.get_or_create(name='mat_1', young=10000000, poisson=0.3)
        )
        Beam.get_or_create(
            start_node=Node.get(x=4, y=3),
            end_node=Node.get_or_create(x=8, y=0),
            section=Section.get(name='sect_1', area=0.02, inertia=0.001),
            material=Material.get(name='mat_1', young=10000000, poisson=0.3)
        )
        Support.get_or_create(
            node=Node.get(x=0, y=0),
            x=False,
            y=True,
            rot=False
        )
        Support.get_or_create(
            node=Node.get(x=8, y=0),
            x=True,
            y=True,
            rot=False
        )
        Force.get_or_create(
            node=Node.get(x=4, y=3),
            mgn_x=0,
            mgn_y=-10
        )
        Force.get_or_create(
            node=Node.get(x=0, y=0),
            mgn_x=5,
            mgn_y=0
        )
        self.fem = FEM()

    def test_local_k(self):
        expected = Matrix([
            [4.0e7, 0.0, 0.0, -4.0e7, 0.0, 0.0],
            [0.0, 9.6e5, 2.4e6, 0.0, -9.6e5, 2.4e6],
            [0.0, 2.4e6, 8.0e6, 0.0, -2.4e6, 4.0e6],
            [-4.0e7, 0.0, 0.0, 4.0e7, 0.0, 0.0],
            [0.0, -9.6e5, -2.4e6, 0.0, 9.6e5, -2.4e6],
            [0.0, 2.4e6, 4.0e6, 0.0, -2.4e6, 8.0e6],
        ])
        for beam in Beam.objects:
            self.assertEqual(self.fem._generate_single_local_stiffness_matrix(beam), expected)

    def test_local_direction_matrix(self):
        expected = Matrix([
            [0.8, 0.6, 0.0, 0.0, 0.0, 0.0],
            [-0.6, 0.8, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.8, 0.6, 0.0],
            [0.0, 0.0, 0.0, -0.6, 0.8, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        ])
        self.assertEqual(
            self.fem._generate_single_directional_matrix(
                beam=Beam.get(_id=1)
            ),
            expected
        )
        self.assertEqual(
            self.fem._generate_single_directional_matrix(
                beam=Beam.get(_id=2)
            ),
            Ops().transpose(expected)
        )

    def test_single_global_k_beam_1(self):
        expected = Matrix([
            [25945600, -18739200, 1440000, -25945600, 18739200, 1440000],
            [-18739200, 15014400, 1920000, 18739200, -15014400, 1920000],
            [1440000, 1920000, 8000000, -1440000, -1920000, 4000000],
            [-25945600, 18739200, -1440000, 25945600, -18739200, -1440000],
            [18739200, -15014400, -1920000, -18739200, 15014400, -1920000],
            [1440000, 1920000, 4000000, -1440000, -1920000, 8000000],
        ])
        beam = Beam.get(_id=1)
        k_local = self.fem._generate_single_local_stiffness_matrix(beam)
        k_global = self.fem._transform_local_to_global(beam, k_local)
        self.assertEqual(k_global, expected)

    def test_single_global_k_beam_2(self):
        expected = Matrix([
            [25945600, 18739200, -1440000, -25945600, -18739200, -1440000],
            [18739200, 15014400, 1920000, -18739200, -15014400, 1920000],
            [-1440000, 1920000, 8000000, 1440000, -1920000, 4000000],
            [-25945600, -18739200, 1440000, 25945600, 18739200, 1440000],
            [-18739200, -15014400, -1920000, 18739200, 15014400, -1920000],
            [-1440000, 1920000, 4000000, 1440000, -1920000, 8000000],
        ])
        beam = Beam.get(_id=2)
        k_local = self.fem._generate_single_local_stiffness_matrix(beam)
        k_global = self.fem._transform_local_to_global(beam, k_local)
        self.assertEqual(k_global, expected)
