from src.models.material import Material
from src.models.meta import Base
from src.models.node import Node
from src.models.section import Section


class Beam(Base):
    objects = []
    name = 'Beam'

    def __init__(self, start_node=None, end_node=None, section=None, material=None):
        Beam.objects.append(self)
        self._id = len(Beam.objects)
        self.start_node = start_node
        self.end_node = end_node
        self.section = section
        self.material = material

    def __repr__(self):
        return "Beam #{id}".format(id=self._id)
