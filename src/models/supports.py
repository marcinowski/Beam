from src.models.meta import Base


class Support(Base):
    object = []
    name = 'Support'

    def __init__(self, node=None, x=None, y=None, rot=None):
        self.node = node
        self.x = x
        self.y = y
        self.rot = rot

    def __repr__(self):
        blocked = [direction for direction in ['x', 'y', 'rot'] if getattr(self, direction) is True]
        return 'Support at {node}, blocked directions: {block}'.format(node=self.node, block=blocked)


class Joint(Base):
    object = []
    name = 'Joint'

    def __init__(self, node=None, x=None, y=None, rot=None):
        self.node = node
        self.x = x
        self.y = y
        self.rot = rot

    def __repr__(self):
        released = [direction for direction in ['x', 'y', 'rot'] if getattr(self, direction) is True]
        return 'Support at {node}, released directions: {released}'.format(node=self.node, released=released)
