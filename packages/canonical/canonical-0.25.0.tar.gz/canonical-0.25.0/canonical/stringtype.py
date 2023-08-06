# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import Generator

from pydantic.validators import str_validator


class StringType(str):
    """Base class for string types."""
    __module__: str = 'canonical'
    openapi_title: str | None = None
    openapi_format: str | None = None

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None:
        field_schema.update( # pragma: no cover
            title=cls.openapi_title or cls.__name__,
            type='string'
        )
        if cls.openapi_format:
            field_schema.update(format=cls.openapi_format)

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., str | None], None, None]:
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> str:
        raise NotImplementedError

    def __repr__(self) -> str: # pragma: no cover
        return f'{type(self).__name__}({self})'