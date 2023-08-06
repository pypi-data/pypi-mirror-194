# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generic
from typing import TypeVar

from .messageheader import MessageHeader

T = TypeVar('T')


class Envelope(MessageHeader, Generic[T]):

    def dict(self, *args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault('by_alias', True)
        return super().dict(*args, **kwargs)