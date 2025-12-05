from __future__ import annotations

from typing import TypeVar

from .base import BaseRepository
from ..models import Person

T = TypeVar('T', bound=Person)


class PersonRepository(BaseRepository[T]):
    def __init__(self, model_cls: type[T]) -> None:
        super().__init__(
            model_cls=model_cls
        )