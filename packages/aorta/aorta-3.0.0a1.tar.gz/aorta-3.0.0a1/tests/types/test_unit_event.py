# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable

import pytest

import aorta
from aorta.types.test.messagetype import *


class FooEvent(aorta.Event):
    foo: int


@pytest.fixture # type: ignore
def message() -> aorta.Event:
    return FooEvent(foo=1)


@pytest.fixture # type: ignore
def typecheck() -> Callable[[aorta.types.MessageHeader], bool]:
    return aorta.types.MessageHeader.is_event


@pytest.fixture # type: ignore
def parse() -> Callable[[Any], aorta.types.Envelope[Any] | None]:
    return aorta.types.EventType.parse