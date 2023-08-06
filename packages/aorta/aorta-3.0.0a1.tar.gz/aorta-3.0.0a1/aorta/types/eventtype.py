# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic
import pydantic.main

from .envelope import Envelope
from .messageheader import MessageHeader


class EventType(pydantic.main.ModelMetaclass):
    __registry__: dict[tuple[str, str], type[Envelope[Any]]] = {}
    typename: str = 'unimatrixone.io/event'

    @staticmethod
    def parse(data: Any) -> Envelope[Any] | None:
        try:
            header = MessageHeader.parse_obj(data)
            if header.type == EventType.typename:
                return EventType.__registry__[(header.api_version, header.kind)].parse_obj(data)
        except (pydantic.ValidationError, KeyError, TypeError, ValueError):
            return None

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ) -> 'EventType':
        is_abstract = namespace.pop('__abstract__', False)
        new_class =  super().__new__(cls, name, bases, namespace, **params) # type: ignore
        namespace.setdefault('__version__', 'v1')
        if not is_abstract:
            k: tuple[str, str] = (namespace['__version__'], name)
            if k in cls.__registry__:
                raise TypeError('Message {0}/{1} is already registered.'.format(*k))
            new_class.__envelope__ = type(
                f'{name}Envelope',
                (Envelope,), # type: ignore
                {
                    '__annotations__': {
                        'data': new_class
                    }
                }
            )
            cls.__registry__[k] = new_class.__envelope__ # type: ignore
        
        return new_class # type: ignore