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
from .types import Command
from .types import MessageHandlerType


class CommandHandlerMetaclass(MessageHandlerType):
    handles: type[Command] = Command
    parameter_name: str = 'command'


class CommandHandler(MessageHandler, metaclass=CommandHandlerMetaclass):
    __module__: str = 'aorta'
    __abstract__: bool = True

    async def handle(self, command: Any) -> Any:
        raise NotImplementedError