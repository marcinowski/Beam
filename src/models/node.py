from src.models.meta import Base, ObjectDoesNotExist


class Node(Base):
    """ Node Class and all business logic.
    """
    objects = []
    name = 'Node'

    def __init__(self, x=None, y=None):
        """ Method takes named arguments x and y.
        """
        Node.objects.append(self)
        self._id = len(Node.objects)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Node at (x,y) = ({},{})'.format(self.x, self.y)

    @classmethod
    def get_node_by_id(cls, obj_id):
        """ Gets a node by it's unique global_id, raises NodeDoesNotExist if such node is not found.
        """
        for obj in cls.objects:
            if obj.id == obj_id:
                return obj
        raise ObjectDoesNotExist('No node with that id.')
