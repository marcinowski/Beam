from src.models.material import Material
from src.models.meta import Base
from .node import Node
from .section import Section


class Beam(Base):
    objects = []
    name = 'Beam'

    def __init__(self, start_node=None, end_node=None, section=None, material=None):
        Beam.objects.append(self)
        self._id = len(Beam.objects)
        self.start_node = start_node or self.set_node()
        self.end_node = end_node or self.set_node()
        self.section = section or self.set_section()
        self.material = material or self.set_material()

    @staticmethod
    def set_node():  # FIXME: Each of these set methods should be moved to corresponding enitity!
        print('Create a point: \n')
        x = input('\tX: ')
        y = input('\tY: ')
        return Node.get_or_create(x=x, y=y)

    @staticmethod
    def set_section():
        print('Create a section: \n')
        name = input('\tName: ')
        area = input('\tArea: ')
        inertia = input('\tInertia: ')
        return Section.get_or_create(name=name, area=area, inertia=inertia)

    @staticmethod
    def set_material():
        print('Create a material: \n')
        name = input('\tName: ')
        young = input('\tYoung: ')
        poisson = input('\tPoisson: ')
        return Material.get_or_create(name=name, young=young, poisson=poisson)

    def detect_duplicates(self):
        pass

    def edit(self):
        pass
