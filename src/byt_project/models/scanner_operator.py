from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, TYPE_CHECKING, Any, cast

from .base import BaseModel
from .employee import Employee

if TYPE_CHECKING:
    from .scanner import Scanner


@dataclass(kw_only=True)
class ScannerOperator(Employee):
    MODEL_TYPE: ClassVar[str] = "scanner_operator"

    authorized_scanner_types: list[str]
    incidents_reported: int

    scanner_ids: list[Scanner] | None = field(default_factory=list, init=False)
    scanners: list[Scanner] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()

        # authorized_scanner_types — basic validation
        if not isinstance(self.authorized_scanner_types, list):
            raise TypeError("authorized_scanner_types must be a list")
        if len(self.authorized_scanner_types) == 0:
            raise ValueError("authorized_scanner_types cannot be empty")

        # incidents_reported
        if not isinstance(self.incidents_reported, int) or self.incidents_reported < 0:
            raise ValueError("incidents_reported must be a non-negative integer")

        # scanners — must be list
        if not isinstance(self.scanners, list):
            raise TypeError("scanners must be a list")

        # simple validation of list content
        for s in self.scanners:
            if not isinstance(s, Scanner):
                raise TypeError("all items in scanners must be Scanner instances")

        # Fill scanner_ids automatically from scanners list
        # self.scanner_ids = [
        #     s.id for s in self.scanners
        #     if getattr(s, "id", None) is not None
        # ]

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
