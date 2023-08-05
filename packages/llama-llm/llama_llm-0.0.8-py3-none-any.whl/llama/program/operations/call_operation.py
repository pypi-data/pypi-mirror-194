from llama.program.value import Value

import json


class CallOperation(Value):
    def __init__(self, target_function, input_value, output_value):
        super().__init__(get_type(output_value))
        self._target_function = target_function
        self._input_value = input_value

    def _to_dict(self):
        if isinstance(self._input_value, Value):
            input_value = self._input_value.index
        else:
            input_value = {
                "data": self._input_value.dict(),
                "type": json.loads(type(self._input_value).schema_json()),
            }

        return {
            "name": "CallOperation",
            "function_name": self._target_function.name,
            "input_value": input_value,
        }


def get_type(output_value):
    if isinstance(output_value, tuple):
        return (value.type for value in output_value)

    return output_value._type
