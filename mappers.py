from functools import reduce


def int_mapper(object_attr_name, base_key=None):
    def _handler(host_object, _json_data, json_key):
        json_data = _json_data

        if base_key is not None and base_key in json_data:
            json_data = json_data[base_key]

        value = None
        if json_key in json_data:
            try:
                value = int(json_data[json_key])
            except ValueError:
                value = None
        setattr(host_object, object_attr_name, value)

    return _handler


def boolean_mapper(object_attr_name, is_numeric=False, base_key=None):
    def _handler(host_object, _json_data, json_key):
        json_data = _json_data

        if base_key is not None and base_key in json_data:
            json_data = json_data[base_key]

        value = False
        if json_key in json_data:
            value = json_data[json_key] == (1 if is_numeric else 'Y')
        setattr(host_object, object_attr_name, value)

    return _handler


def string_mapper(object_attr_name, base_key=None):
    def _handler(host_object, _json_data, json_key):
        json_data = _json_data

        if base_key is not None and base_key in json_data:
            json_data = json_data[base_key]

        value = None
        if json_key in json_data:
            try:
                value = str(json_data[json_key])
            except ValueError:
                value = None
        setattr(host_object, object_attr_name, value)

    return _handler


def object_list_mapper(object_attr_name, klass, sort_key='', sort_asc=True):
    def _handler(host_object, json_data, json_key):
        values = []
        if json_key in json_data:
            values = list(map(lambda d: klass(d), json_data[json_key]))
            if reduce(lambda acc, ele: acc and ele, values, True):
                values.sort(key=lambda ele: getattr(ele, sort_key), reverse=not sort_asc)

        setattr(host_object, object_attr_name, values)

    return _handler
