class Mappable(type):
    @property
    def mappings(cls):
        return cls._mappings

class MappableObject(object, metaclass=Mappable):
    _mappings = {}

    def __init__(self, json_data):
        for json_key, handler in self.__class__.mappings.items():
            handler(self, json_data, json_key)
