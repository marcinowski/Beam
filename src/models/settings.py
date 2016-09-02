from src.models.meta import Base


class Settings(Base):
    objects = []
    name = 'Settings'

    def __init__(self):
        Settings.objects.append(self)
        self.length = 1  # this is related to 1m
        self.force = 1000  # this is related to 1N
        self.pressure = 1000  # this is related to 1Pa
        self.time = 1  # this is related to 1s
