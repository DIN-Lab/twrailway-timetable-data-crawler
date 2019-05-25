from mappable import MappableObject
from mappers import *

class TrainStop(MappableObject):
    _mappings = {
        'StationID' : string_mapper('station'),
        'StopSequence' : int_mapper('order'),
        'ArrivalTime' : string_mapper('arrival_time'),
        'DepartureTime' : string_mapper('departure_time')
    }

class Train(MappableObject):
    _mappings = {
        'TrainNo' : string_mapper('number', base_key='TrainInfo'),
        'BreastFeedFlag': boolean_mapper('has_breastfeeding_rooms', is_numeric=True, base_key='TrainInfo'),
        'PackageServiceFlag' : boolean_mapper('carries_packages', is_numeric=True, base_key='TrainInfo'),
        'DiningFlag' : boolean_mapper('has_dining_rooms', is_numeric=True, base_key='TrainInfo'),
        'WheelChairFlag' : boolean_mapper('is_accessible', is_numeric=True, base_key='TrainInfo'),
        'BikeFlag' : boolean_mapper('has_bike_stands', is_numeric=True, base_key='TrainInfo'),
        'TrainTypeID' : string_mapper('train_class', base_key='TrainInfo'),
        'Direction': string_mapper('direction', base_key='TrainInfo'),
        'StopTimes': object_list_mapper('stops', TrainStop, 'order')
    }

    def __init__(self, json_data):
        for json_key, handler in self.__class__.mappings.items():
            handler(self, json_data, json_key)
