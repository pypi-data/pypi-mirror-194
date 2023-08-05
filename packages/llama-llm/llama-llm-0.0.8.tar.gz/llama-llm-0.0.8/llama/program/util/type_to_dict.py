from llama.program.value import Value
from llama.types.base_specification import BaseSpecification

import json


def type_to_dict(type):
    if type == BaseSpecification:
        return json.loads(self._type.schema_json()),

    return {"type": str(type)}


def value_to_dict(input_value):
    if isinstance(input_value, Value):
        return input_value._index

    return {
        "data": rewrite_dict_data(input_value),
        "type": rewrite_dict_type(input_value),
    }


def rewrite_dict_data(input_value):
    if isinstance(input_value, Value):
        return input_value._index
    elif isinstance(input_value, BaseSpecification):
        input_value = input_value.dict()
        for key, value in input_value.items():
            input_value[key] = rewrite_dict_data(value)

    return input_value


def rewrite_dict_type(input_value):
    assert isinstance(input_value, BaseSpecification)
    return json.loads(type(input_value).schema_json())
