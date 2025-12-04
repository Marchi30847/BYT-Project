from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass, field
from typing import Any, ClassVar, Protocol, Mapping, runtime_checkable, Self


@runtime_checkable
class Serializable(Protocol):
    MODEL_TYPE: ClassVar[str]

    def to_dict(self) -> dict[str, Any]:
        ...

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        ...


@dataclass
class BaseModel(Serializable):
    MODEL_TYPE: ClassVar[str] = "base_model"

    id: int | None = field(default=None, init=False)

    def to_dict(self) -> dict[str, Any]:
        if not is_dataclass(self):
            raise TypeError("BaseModel requires dataclass subclasses")

        data: dict[str, Any] = asdict(self)
        data["type"] = self.MODEL_TYPE

        return data

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        if cls is BaseModel:
            raise TypeError("BaseModel.from_dict must be called on a subclass")

        kwargs: dict[str, Any] = dict(data)
        kwargs.pop("type", None)

        raw_id: str | int | None = kwargs.pop("id", None)

        # noinspection PyArgumentList
        instance = cls(**kwargs)

        instance.id = int(raw_id) if raw_id is not None else None

        return instance
