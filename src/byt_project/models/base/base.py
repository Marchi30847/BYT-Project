from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass, field, fields
from typing import Any, ClassVar, Protocol, Mapping, runtime_checkable, Self, Callable


@runtime_checkable
class Serializable(Protocol):
    MODEL_TYPE: ClassVar[str]

    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self: ...


@dataclass(kw_only=True)
class BaseModel(Serializable):
    MODEL_TYPE: ClassVar[str] = "base_model"

    id: int | None = field(default=None, init=False)

    _loaders: dict[str, Callable[..., Any]] = field(
        default_factory=dict, init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None: ...

    def set_loader(self, field_name: str, loader_func: Callable[..., Any]) -> None:
        self._loaders[field_name] = loader_func

    def _run_loader(self, field_name: str, *args, **kwargs) -> Any | None:
        loader: Callable[..., Any] = self._loaders.get(field_name)
        if loader:
            return loader(*args, **kwargs)

        return None

    def _get_fk_value(self, obj_field: Any, id_field_val: int | None) -> int | None:
        if obj_field and hasattr(obj_field, "id"):
            return obj_field.id

        return id_field_val

    def _get_many_fk_value(self, objs_list: list[Any] | None, ids_list: list[int]) -> list[int]:
        if objs_list is None:
            return ids_list

        current_ids: list[int] = [
            obj.id for obj in objs_list
            if obj is not None and getattr(obj, "id", None) is not None
        ]

        if not current_ids and ids_list:
            return ids_list

        return current_ids

    def _remove_cashed_fields(self, data: dict[str, Any]) -> None:
        cashed_fields: set[str] = {f.name for f in fields(type(self)) if f.name.startswith("_")}

        for field_name in cashed_fields:
            data.pop(field_name, None)

    @staticmethod
    def _restore_fk(instance: Any, data: dict[str, Any], key: str, attr_name: str) -> None:
        raw_val: Any = data.get(key)
        val: int = int(raw_val) if raw_val is not None else None
        setattr(instance, attr_name, val)

    @staticmethod
    def _restore_many_fk(instance: Any, data: dict[str, Any], key: str, attr_name: str) -> None:
        raw_ids: Any = data.get(key)
        if isinstance(raw_ids, list):
            clean_ids: list[int] = [int(x) for x in raw_ids if x is not None]
            setattr(instance, attr_name, clean_ids)

    def to_dict(self) -> dict[str, Any]:
        if not is_dataclass(self):
            raise TypeError("BaseModel requires dataclass subclasses")

        data: dict[str, Any] = asdict(self)

        data["type"] = self.MODEL_TYPE

        self._remove_cashed_fields(data)

        return data

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        if cls is BaseModel:
            raise TypeError("BaseModel.from_dict must be called on a subclass")

        valid_arg_names: set[str] = {f.name for f in fields(cls) if f.init}
        kwargs: dict[str, Any] = {k: v for k, v in data.items() if k in valid_arg_names}

        # noinspection PyArgumentList
        instance = cls(**kwargs)

        raw_id: str | int | None = data.get("id")
        instance.id = int(raw_id) if raw_id is not None else None

        return instance
