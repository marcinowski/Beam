from collections import namedtuple


class ObjectExists(Exception):
    pass


class ObjectDoesNotExist(Exception):
    pass


class MultipleObjectsFound(Exception):
    pass


class Meta(type):
    def __call__(cls, **params):
        for elem in cls.objects:
            if cls.check_params(elem, **params):
                raise ObjectExists('Object already exists!')
        return super(Meta, cls).__call__(**params)


class Base(metaclass=Meta):
    objects = []  # Fixme: this may be a class object overriding lists?
    coords = namedtuple('coords', ['x', 'y'])

    @classmethod
    def remove(cls, instance):
        """
        Removes selected instance from objects.
        :param instance: instance of an object
        """
        cls.objects.remove(instance)
        cls._sort_global_ids()

    @classmethod
    def count(cls):
        """
        Returns number of created objects.
        :return: number of objects
        """
        return len(cls.objects)

    @classmethod
    def remove_all(cls):
        """
        Removes all created objects.
        """
        for instance in cls.objects:
            cls.remove(instance)

    def modify_parameters(self, **kwargs):
        """ Method for modifying given parameters
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get(cls, **params):
        """ Gets a node by it's parameters
        """
        results = cls.get_multiple(**params)
        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            raise ObjectDoesNotExist
        else:
            raise MultipleObjectsFound

    @classmethod
    def get_multiple(cls, **params):
        return [obj for obj in cls.objects if cls.check_params(obj, **params)]

    @classmethod
    def check_params(cls, obj, **params):
        for key, value in params.items():
            if getattr(obj, key) != value:
                return False
        return True

    @classmethod
    def get_or_create(cls, **params):
        """ Gets object with given params or creates one if non-existing.
        :param params: object parameters for filtering
        """
        try:
            obj = cls.get(**params)
        except ObjectDoesNotExist:
            obj = cls(**params)
        except MultipleObjectsFound:
            raise MultipleObjectsFound
        return obj

    @staticmethod
    def _set_param(param):
        """ Method for setting given parameters, by now it's being done manually.
        """
        value = input('Set {} param: '.format(param))
        return value

    @classmethod
    def _sort_global_ids(cls):
        """ Function should clean up the global_ids list, so that when creating or deleting a new one a test will run
        to check if all the ids are in proper use.
        """
        for i, obj in enumerate(cls.objects):
            obj._id = i + 1
