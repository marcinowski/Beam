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
        self.loads = Force.objects + Momentum.objects + UniformLoad.objects
        self.supports = Support.objects
        self.joints = Joint.objects

    def run_calculations(self):
        pass

    def check_beam_connections(self):
        """Method should check if no beams are disconnected"""
        pass

    def generate_global_stiffness_matrix(self):
        for beam in self.beams:
            k_local = self._generate_single_local_stiffness_matrix(beam)
            k_global = self._transform_local_to_global(beam, k_local)

    def generate_load_vector(self):
        pass

    def _transform_local_to_global(self, beam, k_local):
        length = beam.length() * self.settings.length
        sinus = (beam.end_node.y - beam.start_node.y) / length
        cosinus = (beam.end_node.x - beam.start_node.x) / length
        c_matrix = m_temp.create_directional_matrix(c=cosinus, s=sinus)
        c_transpose = Ops().transpose(c_matrix)
        c_k_loc = Ops().multiply(c_matrix, k_local)
        return Ops().multiply(c_k_loc, c_transpose)

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
