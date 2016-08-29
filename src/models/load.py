from src.models.meta import Base


class Force(Base):
    objects = []
    name = 'Force'

    def __init__(self, node=None, mgn_x=None, mgn_y=None):
        Force.objects.append(self)
        self._id = len(Force.objects)
        self.node = node
        self.mgn_x = mgn_x
        self.mgn_y = mgn_y

    def __repr__(self):
        return "Concentrated Force at {node} " \
               "with magnitudes (x,y): ({mgn_x},{mgn_y])"\
            .format(
                node=self.node,
                mgn_x=self.mgn_x,
                mgn_y=self.mgn_y
            )


class Momentum(Base):
    objects = []
    name = 'Momentum'

    def __init__(self, node=None, value=None):
        Momentum.objects.append(self)
        self._id = len(Momentum.objects)
        self.node = node
        self.value = value

    def __repr__(self):
        return "Momentum at {node} of magnitude {value}"\
            .format(
                node=self.node,
                value=self.value,
            )


class UniformLoad(Base):
    objects = []
    name = 'Uniform Load'

    def __init__(self, beam=None, mgn_x=None, mgn_y=None):
        UniformLoad.objects.append(self)
        self._id = len(UniformLoad.objects)
        self.beam = beam
        self.mgn_x = mgn_x
        self.mgn_y = mgn_y

    def __repr__(self):
        return "Uniform Load at {beam} of magnitude (x,y): ({mgn_x},{mgn_y])"\
            .format(
                beam=self.beam,
                mgn_x=self.mgn_x,
                mgn_y=self.mgn_y
            )
