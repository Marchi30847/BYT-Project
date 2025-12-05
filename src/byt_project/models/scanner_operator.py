from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .employee import Employee

if TYPE_CHECKING:
    from .scanner import Scanner


@dataclass(kw_only=True)
class ScannerOperator(Employee):
    MODEL_TYPE: ClassVar[str] = "scanner_operator"

    authorized_scanner_types: list[str]
    incidents_reported: int

    _scanners: list[Scanner] | None = field(default=None, init=False, repr=False)

    @property
    def scanners(self) -> list[Scanner]:
        if self._scanners is not None:
            return self._scanners

        if self.id is not None:
            loaded: list[Scanner] | None = self._run_loader("scanners", self.id)
            if loaded is not None:
                self._scanners = loaded
                return self._scanners

        self._scanners = []
        return self._scanners

    @scanners.setter
    def scanners(self, value: list[Scanner]) -> None:
        self._scanners = value

    def __post_init__(self) -> None:
        super().__post_init__()

        if len(self.authorized_scanner_types) == 0:
            raise ValueError("Authorized scanner types cannot be empty")

        if self.incidents_reported < 0:
            raise ValueError("Incidents reported must be a non-negative integer")

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ScannerOperator:
        data_copy: dict[str, Any] = dict(data)

        instance = cast(ScannerOperator, super().from_dict(data_copy))

        return instance

    def report_incident(self, description: str) -> None:
        print(f"Operator {self.id} reporting incident: {description}")
