from src.models.beam import Beam
from src.models.load import Force, Momentum, UniformLoad
from src.models.supports import Support, Joint
from src.fem.matrix_ops import MatrixOperations


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
            self._generate_single_local_stif_matrix(beam)

    def generate_load_vector(self):
        pass

    def transform_local_to_global(self):
        pass

    def generate_global_stiffness_matrix(self):
        pass

    def _generate_single_local_stif_matrix(self, beam):
        l = ((beam.start_node.x - beam.end_node.x) ** 2 + (beam.start_node.y - beam.end_node.y) ** 2) ** 0.5
        e = beam.material.young
        a = beam.section.area
        i = beam.section.inertia
        dn = e * a / l
        db = (12 * e * i / l ** 3, 6 * e * i / l ** 2, 4 * e * i / l)
        k = [[dn, 0, 0],
             [0, db[0], db[1]],
             [0, db[1], db[2]]]
