from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, ClassVar, Protocol, Mapping, runtime_checkable, Self
import json


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

    def to_dict(self) -> dict[str, Any]:
        if not is_dataclass(self):
            raise TypeError("BaseModel requires dataclass subclasses")

        data = asdict(self)
        data["type"] = self.MODEL_TYPE
        return data

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        if cls is BaseModel:
            raise TypeError("BaseModel.from_dict must be called on a subclass")

        kwargs = dict(data)
        kwargs.pop("type", None)
        return cls(**kwargs)

    def to_json(self, *, indent: int | None = None) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls: type[Self], json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))
