from itertools import product

from src.models.beam import Beam
from src.models.node import Node
from src.models.settings import Settings
from src.models.load import Force, Momentum, UniformLoad
from src.models.supports import Support, Joint
from src.fem.matrix_ops import MatrixOperations as Ops
from src.fem.matrix_ops import Matrix
from src.fem.matrix_templates import LOCAL_MATRIX_MULTIPLIERS as multiplier
from src.fem.matrix_templates import LOCAL_MATRIX_LENGTH_POWERS as power
from src.fem import matrix_templates as m_temp


class FEM(object):
    def __init__(self):
        self.beams = Beam.objects
        self.nodes = Node.objects
        self.settings = Settings.objects[0]
        self.forces = Force.objects
        self.forces = Momentum.objects
        # self.uniform_loads = UniformLoad.objects
        self.supports = Support.objects
        self.joints = Joint.objects
        self.global_k = Ops().create_empty_matrix(Node.count()*3)
        self.displacement_v = []
        self.force_v = []

    def run_calculations(self):
        pass

    def check_beam_connections(self):
        """Method should check if no beams are disconnected"""
        pass

    def generate_global_stiffness_matrix(self):
        for beam in self.beams:
            k_local = self._generate_single_local_stiffness_matrix(beam)
            single_k_global = self._transform_local_to_global(beam, k_local)
            self._map_single_k_onto_global_k(single_k_global, beam, self.global_k)

    def generate_load_vector(self):
        pass

    def generate_displacement_vector(self):
        init = ['u' for _ in Node.count()*3]
        for sup in self.supports:
            pos = sup.node._id * 3
            for i, j in enumerate(['x', 'y', 'rot']):
                if getattr(sup, j):
                    init[pos + i] = 0
        self.displacement_v = init

    def _map_single_k_onto_global_k(self, k, beam, global_k):
        start_pos = beam.start_node._id - 1
        end_pos = beam.end_node._id - 1
        pos = tuple(product((start_pos, end_pos), repeat=2))
        k_copy = self._divide_k_into_four(k)
        for index, sub_m in enumerate(k_copy):
            for i in range(3):
                for j in range(3):
                    global_k[pos[index][0] * 3 + i][pos[index][1] * 3 + j] += sub_m[i][j]

    def _divide_k_into_four(self, k_matrix):
        ranges = ((0, 3), (3, 6))
        result = Matrix([])
        for rows in ranges:
            for cols in ranges:
                result.append(
                    [[k_matrix[i][j] for j in range(*cols)] for i in range(*rows)]
                )
        return result

    def _transform_local_to_global(self, beam, k_local):
        c_matrix = self._generate_single_directional_matrix(beam)
        c_transpose = Ops().transpose(c_matrix)
        c_k_loc = Ops().multiply(c_matrix, k_local)
        return Ops().multiply(c_k_loc, c_transpose)

    def _generate_single_directional_matrix(self, beam):
        length = beam.length() * self.settings.length
        sinus = (beam.end_node.y - beam.start_node.y) / length
        cosinus = (beam.end_node.x - beam.start_node.x) / length
        return m_temp.create_directional_matrix(c=cosinus, s=sinus)

    def _generate_single_local_stiffness_matrix(self, beam):
        length = beam.length() * self.settings.length
        e_young = beam.material.young * self.settings.pressure
        area = beam.section.area * self.settings.length**2
        inertia = beam.section.inertia * self.settings.length**4
        dn = e_young * area
        db = e_young * inertia
        size = range(len(power))
        k = Matrix([[db * multiplier[i][j] / (length ** power[i][j]) for j in size] for i in size])
        for i in size:
            if i % 3 == 0:
                for j in size:
                    k[i][j] *= dn/db
        return k
