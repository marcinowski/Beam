from src.models.meta import Base


class Section(Base):
    objects = []
    name = 'Section'

    def __init__(self, name=None, area=None, inertia=None):
        """ Creates a Section object with parameters name, A (Area), I (Inertia)
        """
        Section.objects.append(self)
        self._id = len(Section.objects)
        self.name = name
        self.area = area
        self.inertia = inertia

    def __repr__(self):
        return 'Section {} - area: {}, inertia: {}'.format(self.name, self.area, self.inertia)
