from src.models.beam import Beam
from src.models.load import Force, Momentum, UniformLoad
from src.models.supports import Support, Joint
from src.fem.matrix_ops import MatrixOperations as Ops
from src.fem.matrix_ops import Matrix
from src.fem.matrix_templates import SINGLE_LOCAL_MATRIX_MULTIPLIERS as multiplier
from src.fem.matrix_templates import SINGLE_LOCAL_MATRIX_POWERS_IN_DENOMINATOR as power


class FEM(object):
    def __init__(self):
        self.beams = Beam.objects
        self.loads = Force.objects + Momentum.objects + UniformLoad.objects
        self.supports = Support.objects
        self.joints = Joint.objects

    # def statical_determinity(self):
    #     """This method should check if the amount of support and joints ensures the stability"""
    #     blocked_dirs = len([block for obj in self.supports for block in obj.__dir__.values() if block is True])
    #     blocked_joints = len([block for obj in self.joints for block in obj.__dir__.values() if block is False])
    #     return blocked_dirs - (len(self.beams) - blocked_joints)*3 > 0

    def run_calculations(self):
        pass

    def check_beam_connections(self):
        """Method should check if no beams are disconnected"""
        pass

    def generate_local_stiffness_matrix(self):
        for beam in self.beams:
            self._generate_single_local_stiffness_matrix(beam)

    def generate_load_vector(self):
        pass

    def transform_local_to_global(self):
        pass

    def generate_global_stiffness_matrix(self):
        pass

    @staticmethod
    def _generate_single_local_stiffness_matrix(beam):
        l = ((beam.start_node.x - beam.end_node.x) ** 2 + (beam.start_node.y - beam.end_node.y) ** 2) ** 0.5
        e = beam.material.young
        a = beam.section.area
        i = beam.section.inertia
        dn = e * a
        db = e * i
        size = range(len(power))
        k = Matrix([[db * multiplier[i][j] / (l ** power[i][j]) for j in size] for i in size])
        for i in size:
            if i % 3 == 0:
                for j in size:
                    k[i][j] *= dn/db
        return k


