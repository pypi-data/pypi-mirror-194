# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .messagehandler import MessageHandler
from .types import Event
from .types import MessageHandlerType


class EventListenerMetaclass(MessageHandlerType):
    handles: type[Event] = Event
    parameter_name: str = 'event'


class EventListener(MessageHandler, metaclass=EventListenerMetaclass):
    """Handles event messages."""
    __module__: str = 'aorta'
    __abstract__: bool = True

    async def handle(self, event: Any) -> Any:
        raise NotImplementedError