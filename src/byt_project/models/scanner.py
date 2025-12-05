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

        if not self.model.strip():
            raise ValueError("model must be a non-empty string")
        if self.avgScanTime <= 0:
            raise ValueError("avgScanTime must be a positive number")

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        # 1. Дату в ISO строку
        data["lastCalibration"] = self.lastCalibration.isoformat()

        # 2. Сохраняем список ID операторов (M2M) через хелпер
        data["operator_ids"] = self._get_many_fk_value(self._operators, self.operator_ids)

        # 3. Чистим приватный кэш
        data.pop("_operators", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Scanner:
        data_copy = dict(data)

        # 1. Десериализация даты
        raw_calib: Any = data_copy.get("lastCalibration")
        if isinstance(raw_calib, str):
            data_copy["lastCalibration"] = datetime.fromisoformat(raw_calib)

        # 2. Создание через родителя (BaseModel)
        instance = cast(Scanner, super().from_dict(data_copy))

        # 3. Восстановление списка ID операторов
        cls._restore_many_fk(instance, data, "operator_ids", "operator_ids")

        return instance

    # --- БИЗНЕС-ЛОГИКА ---

    def add_operator(self, operator: ScannerOperator) -> None:
        """Добавляет оператора и синхронизирует списки."""
        # Используем свойство, чтобы инициализировать кэш, если он пуст
        if operator not in self.operators:
            self.operators.append(operator)

            # Поскольку мы обошли сеттер (использовали append),
            # нужно синхронизировать список ID
            if operator.id is not None:
                self.operator_ids.append(operator.id)