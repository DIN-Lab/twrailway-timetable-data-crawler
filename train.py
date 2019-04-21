from mappable import MappableObject
from mappers import *

class TrainStop(MappableObject):
    _mappings = {
        'Station' : string_mapper('station'),
        'Order' : int_mapper('order'),
        'ArrTime' : string_mapper('arrival_time'),
        'DepTime' : string_mapper('departure_time')
    }

class Train(MappableObject):
    _mappings = {
        'Train' : string_mapper('number'),
        'BreastFeed': boolean_mapper('has_breastfeeding_rooms'),
        'Package' : boolean_mapper('carries_packages'),
        'Dining' : boolean_mapper('has_dining_rooms'),
        'Cripple' : boolean_mapper('is_accessible'),
        'Bike' : boolean_mapper('has_bike_stands'),
        'CarClass' : string_mapper('train_class'),
        'LineDir': string_mapper('direction'),
        'TimeInfos': object_list_mapper('stops', TrainStop, 'order')
    }

    def __init__(self, json_data):
        for json_key, handler in self.__class__.mappings.items():
            handler(self, json_data, json_key)
