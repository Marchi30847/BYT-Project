from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, TYPE_CHECKING, Any, cast

from .base import BaseModel

if TYPE_CHECKING:
    from .employee import Employee
    from .scanner import Scanner


@dataclass(kw_only=True)
class ScannerOperator(BaseModel, Employee):
    MODEL_TYPE: ClassVar[str] = "scanner_operator"

    authorized_scanner_types: list[str]
    incidents_reported: int

    scanner_ids: list[Scanner] | None = field(default_factory=list, init=False)
    scanners: list[Scanner] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.authorized_scanner_types) not in (1, 2):
            raise ValueError("ScannerOperator must have 1 or 2 authorized scanner types")

        self.scanner_ids.id = [s.id for s in self.scanners if getattr(s, 'id', None) is not None]

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        if self.scanners:
            data["scanner_ids"] = [s.id for s in self.scanners if getattr(s, 'id', None) is not None]
        else:
            data["scanner_ids"] = None

        data.pop("scanners", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ScannerOperator:
        instance = cast(ScannerOperator, super().from_dict(data))

        raw_scanners_ids: list | None = data.get("scanner_ids")
        instance.scanner_ids = list(raw_scanners_ids) if all(isinstance(s, int) for s in raw_scanners_ids) else None

        return instance

    def report_incident(self, description: str) -> None:
        raise NotImplementedError
