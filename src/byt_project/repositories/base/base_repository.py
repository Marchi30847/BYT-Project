from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar, Generic, Type, Any

from src.byt_project.models import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class BaseRepository(Generic[T]):
    model_cls: Type[T]
    data_dir: Path = Path("data")
    _next_id: int = field(init=False, default=1)

    def __post_init__(self) -> None:
        self.data_dir.mkdir(exist_ok=True)
        self._init_next_id_from_meta()

    @property
    def model_type(self) -> str:
        return self.model_cls.MODEL_TYPE

    def _get_model_dir(self) -> Path:
        path = self.data_dir / self.model_type
        path.mkdir(exist_ok=True)
        return path

    def _table_path(self) -> Path:
        return self._get_model_dir() / "table.json"

    def _meta_path(self) -> Path:
        return self._get_model_dir() / "meta.json"

    def _load_rows(self) -> list[dict]:
        path = self._table_path()
        if not path.exists():
            return []

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save_rows(self, rows: list[dict]) -> None:
        path = self._table_path()
        with path.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

    def _init_next_id_from_meta(self) -> None:
        meta_path = self._meta_path()
        if not meta_path.exists():
            return

        with meta_path.open("r", encoding="utf-8") as f:
            meta = json.load(f)

        next_id = meta.get("next_id")
        if isinstance(next_id, int) and next_id > 0:
            self._next_id = next_id

    def _persist_next_id(self, rows: list[dict]) -> None:
        if rows:
            max_id = max(row.get("id", 0) or 0 for row in rows)
            if max_id >= self._next_id:
                self._next_id = max_id + 1

        meta = {"next_id": self._next_id}
        meta_path = self._meta_path()
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    def _inject_dependencies(self, rows: list[dict]) -> None:
        ...

    def create(self, obj: T) -> T:
        rows: list[dict[str, Any]] = self._load_rows()

        if obj.id is None:
            obj.id = self._next_id
            self._next_id += 1

        rows.append(obj.to_dict())
        self._save_rows(rows)
        self._persist_next_id(rows)

        return obj

    def find_by_id(self, obj_id: int) -> T | None:
        rows: list[dict[str, Any]] = self._load_rows()
        for row in rows:
            if row.get("id") == obj_id:
                object: T = self.model_cls.from_dict(row)

                self._inject_dependencies(object)

                return object

        return None

    def find_all(self) -> list[T]:
        rows: list[dict[str, Any]] = self._load_rows()

        objects: list[T] = [self.model_cls.from_dict(r) for r in rows]

        for obj in objects:
            self._inject_dependencies(obj)

        return objects

    def update(self, obj: T) -> T | None:
        if obj.id is None:
            raise ValueError("Cannot update object without id")

        rows: list[dict[str, Any]] = self._load_rows()
        updated: bool = False

        for idx, row in enumerate(rows):
            if row.get("id") == obj.id:
                rows[idx] = obj.to_dict()
                updated = True
                break

        if not updated:
            return None

        self._save_rows(rows)
        return obj

    def delete(self, obj_id: int) -> bool:
        rows = self._load_rows()
        new_rows = [r for r in rows if r.get("id") != obj_id]

        if len(new_rows) == len(rows):
            return False

        self._save_rows(new_rows)
        return True
