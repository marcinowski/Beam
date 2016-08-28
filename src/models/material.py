from .meta import Base


class Material(Base):
    objects = []
    name = 'Material'

    def __init__(self, name=None, young=None, poisson=None):  # FIXME: A GROUP? I. E. Concrete, Steel, Wood
        """ Creates a Material object with parameters name, E (Young), v (Poisson),
        """
        Material.objects.append(self)
        self._id = len(Material.objects)
        self.name = name
        self.young = young
        self.poisson = poisson

    def __repr__(self):
        return 'Material {} - E: {}, v: {}'.format(self.name, self.young, self.poisson)
