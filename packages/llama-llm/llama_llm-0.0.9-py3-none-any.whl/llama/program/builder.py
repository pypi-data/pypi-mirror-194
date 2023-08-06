from llama.program.program import Program
from llama.program.function import Function
from llama.program.util.config import edit_config
from llama.program.util.run_ai import query_run_program

from llama.types.type import Type

from llama.program.operations.llama_operation import LlamaOperation
from llama.program.operations.metric_operation import MetricOperation
from llama.program.operations.call_operation import CallOperation
from llama.program.operations.get_element_operation import GetElementOperation
from llama.program.operations.get_field_operation import GetFieldOperation
from llama.program.operations.return_operation import ReturnOperation
from llama.program.operations.feedback_operation import FeedbackOperation

import inspect


class Builder:
    """Build a program for execution by the Llama large language model engine."""

    def __init__(self, name, model_name=None, config={}):
        self.program = Program(self, name)
        self.current_function = self.program.main
        self.value_cache = {}
        self.model_name = model_name
        edit_config(config)

    def __call__(self, input, output_type, *args, **kwargs):
        input_value = input
        if self.model_name is not None:
            kwargs['model_name'] = self.model_name
        new_operation = self.current_function.add_operation(
            LlamaOperation(input_value, output_type, *args, **kwargs)
        )

        return new_operation

    def fit(self, examples=[]):
        self.add_data(examples)

    def add_data(self, data=[]):
        self.program.add_data(examples=data)

    def improve(self, on: str, to: str, good_examples=[], bad_examples=[]):

        new_operation = self.current_function.add_operation(
            FeedbackOperation(
                on=on, to=to, good_examples=good_examples, bad_examples=bad_examples
            )
        )

        return new_operation

    def function(self, function):
        signature = inspect.signature(function)
        input_types = [value.annotation for value in signature.parameters.values()]

        main = self.current_function
        new_function = Function(
            program=self.program, name=function.__name__, input_arguments=input_types
        )
        self.program.functions[new_function.name] = new_function
        self.current_function = new_function
        output_value = function(*new_function.operations)
        self.current_function.add_operation(ReturnOperation(output_value))
        self.current_function = main

        return Lambda(self, new_function, output_value)

    def add_call(self, function, input_value, output_value):
        new_operation = self.current_function.add_operation(
            CallOperation(function, input_value, output_value)
        )

        result = new_operation

        if isinstance(output_value, tuple):
            result = []

            for index, value in enumerate(output_value):
                result.append(
                    self.current_function.add_operation(
                        GetElementOperation(new_operation, value.type, index)
                    )
                )

        return result

    def get_field(self, value, field_name):
        return self.current_function.add_operation(
            GetFieldOperation(value, value._type._get_field_type(field_name), field_name)
        )

    def add_metric(self, metric):
        new_operation = self.current_function.add_operation(
            MetricOperation(metric.input, metric.get_metric_type())
        )

        return new_operation

    def make_metric(
        self, input: Type, metric_type: type, fit: bool = True, higher_is_better=True
    ):
        new_operation = self.current_function.add_operation(
            MetricOperation(input, metric_type)
        )

        return new_operation

    def metrics(self):
        requested_values = [
            op._index for op in self.program.functions["main"].operations
        ]

        params = {
            "program": self.program.to_dict(),
            "requested_values": requested_values,
        }
        response = query_run_program(params)
        response.raise_for_status()

        data = [result[str(index)]["data"] for index in requested_values]

        return data


class Lambda:
    def __init__(self, builder: Builder, function: Function, output_value: Type):
        self.output_value = output_value
        self.builder = builder
        self.function = function

    def __call__(self, *args, **kwargs):
        input_value = self._get_input(*args, **kwargs)
        return self.builder.add_call(self.function, input_value, self.output_value)

    def _get_input(self, *args, **kwargs):
        # TODO: support more than one input LLM arg

        if len(args) > 0:
            return args[0]

        return next(iter(kwargs.values()))
