# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
import types
import typing
from typing import Any

from .command import Command
from .event import Event


class MessageHandlerType(type):
    __module__: str = 'aorta.types'
    handles: type[Command | Event]
    parameter_name: str

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ) -> 'MessageHandlerType':
        # Do some checks to ensure that handlers are properly implemented.
        is_abstract = namespace.pop('__abstract__', False)
        new_class = super().__new__(cls, name, bases, {**namespace, 'handles': []})
        if is_abstract:
            return new_class

        # Ensure that the handle() method accepts the message as the first
        # parameter.
        sig = inspect.signature(new_class.handle) # type: ignore
        parameters = list(sig.parameters.values())
        if len(parameters) < 2:
            raise TypeError(
                f"Invalid number of arguments for {name}.handle(). "
                f"Ensure that the parameters accepted by this method are at "
                f"least {name}.handle(self, {cls.parameter_name}: "
                f"{cls.handles.__name__})."
            )

        arg = parameters[1]
        if arg.name != cls.parameter_name:
            raise TypeError(
                f'The first positional argument to {name}.handle() '
                f'must be named `{cls.parameter_name}`, got `{arg.name}`.'
            )

        # If the argument is a Union, then it accepts multiple message types.
        # Check if all definitions are of the required type.
        handles = [arg.annotation]
        if typing.get_origin(arg.annotation) in (typing.Union, types.UnionType):
            handles = typing.get_args(arg.annotation)
        for Message in set(handles):
            if not issubclass(Message, cls.handles):
                raise TypeError(
                    f"The first positional argument to {name}.handle() must "
                    "annotate itself with the message type that is handled by "
                    "this implementation."
                )
            new_class.handles.append(Message) # type: ignore

        return new_class