from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .base import BaseModel

if TYPE_CHECKING:
    from .scanner_operator import ScannerOperator


@dataclass(kw_only=True)
class Scanner(BaseModel):
    MODEL_TYPE: ClassVar[str] = "scanner"

    model: str
    lastCalibration: datetime
    avgScanTime: float

    operator_ids: list[int] = field(default_factory=list, init=False)
    _operators: list[ScannerOperator] | None = field(default=None, init=False, repr=False)

    @property
    def operators(self) -> list[ScannerOperator]:
        if self._operators is not None:
            return self._operators

        if self.operator_ids:
            loaded: list[ScannerOperator] | None = self._run_loader("operators", self.operator_ids)
            if loaded is not None:
                self._operators = loaded
                return self._operators

        self._operators = []
        return self._operators

    @operators.setter
    def operators(self, value: list[ScannerOperator]) -> None:
        self._operators = value
        self.operator_ids = [s.id for s in value if s.id is not None]


    def __post_init__(self) -> None:
        super().__post_init__()

        # model
        if not isinstance(self.model, str) or not self.model.strip():
            raise ValueError("model must be a non-empty string")

        # lastCalibration
        if not isinstance(self.lastCalibration, datetime):
            raise TypeError("lastCalibration must be a datetime object")

        # avgScanTime
        if not isinstance(self.avgScanTime, (int, float)) or self.avgScanTime <= 0:
            raise ValueError("avgScanTime must be a positive number")

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["lastCalibration"] = self.lastCalibration.isoformat()

        data["operator_ids"] = self._get_many_fk_value(self._operators, self.operator_ids)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Scanner:
        data_copy: dict[str, Any] = dict(data)

        raw_calib: Any = data_copy.get("lastCalibration")
        if isinstance(raw_calib, str):
            data_copy["lastCalibration"] = datetime.fromisoformat(raw_calib)

        instance = cast(Scanner, super().from_dict(data_copy))

        cls._restore_many_fk(instance, data, "operator_ids", "operator_ids")

        return instance


    def add_operator(self, operator: ScannerOperator) -> None:
        if operator not in self.operators:
            self.operators.append(operator)

            if operator.id is not None:
                self.operator_ids.append(operator.id)
