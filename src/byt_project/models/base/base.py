from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass, field, fields
from typing import Any, ClassVar, Protocol, Mapping, runtime_checkable, Self


@runtime_checkable
class Serializable(Protocol):
    MODEL_TYPE: ClassVar[str]

    def to_dict(self) -> dict[str, Any]:
        ...

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        ...


@dataclass(kw_only=True)
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

        valid_arg_names: set[str] = {f.name for f in fields(cls) if f.init}
        kwargs: dict[str, Any] = {k : v for k, v in data.items() if k in valid_arg_names}

        # noinspection PyArgumentList
        instance = cls(**kwargs)

        raw_id: str | int | None = data.get("id")
        instance.id = int(raw_id) if raw_id is not None else None

        return instance
