from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .employee import Employee

if TYPE_CHECKING:
    from .terminal import Terminal
    from .incident import Incident


@dataclass(kw_only=True)
class SecurityOfficer(Employee):
    MODEL_TYPE: ClassVar[str] = "security_officer"

    assigned_zone: str
    is_armed: bool = False
    on_duty: bool = False

    terminal_id: int | None = field(default=None, init=False)
    _terminal: Terminal | None = field(default=None, init=False, repr=False)

    manager_id: int | None = field(default=None, init=False)
    _manager: SecurityOfficer | None = field(default=None, init=False, repr=False)

    _subordinates: list[SecurityOfficer] | None = field(default=None, init=False, repr=False)

    incident_ids: list[int] = field(default_factory=list, init=False)
    _incidents: list[Incident] | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        # assigned_zone
        if not isinstance(self.assigned_zone, str) or not self.assigned_zone.strip():
            raise ValueError("assigned_zone must be a non-empty string")

        # is_armed
        if not isinstance(self.is_armed, bool):
            raise TypeError("is_armed must be a boolean")

        # on_duty
        if not isinstance(self.on_duty, bool):
            raise TypeError("on_duty must be a boolean")

        # terminal_id
        if self.terminal_id is not None and not isinstance(self.terminal_id, int):
            raise TypeError("terminal_id must be int or None")

        # manager_id
        if self.manager_id is not None and not isinstance(self.manager_id, int):
            raise TypeError("manager_id must be int or None")

        # incident_ids - only list check
        if not isinstance(self.incident_ids, list):
            raise TypeError("incident_ids must be a list")

        # _subordinates, _incidents — only check container type, not content
        if self._subordinates is not None and not isinstance(self._subordinates, list):
            raise TypeError("_subordinates must be a list or None")

        if self._incidents is not None and not isinstance(self._incidents, list):
            raise TypeError("_incidents must be a list or None")

    @property
    def terminal(self) -> Terminal | None:
        if self._terminal is not None:
            return self._terminal

        if self.terminal_id is None:
            return None

        loaded: Terminal | None = self._run_loader("terminal", self.terminal_id)
        if loaded:
            self._terminal = loaded

        return self._terminal

    @terminal.setter
    def terminal(self, value: Terminal | None) -> None:
        self._terminal = value
        if value and getattr(value, 'id', None) is not None:
            self.terminal_id = value.id
        else:
            self.terminal_id = None

    # 2. Менеджер
    @property
    def manager(self) -> SecurityOfficer | None:
        if self._manager is not None:
            return self._manager

        if self.manager_id is None:
            return None

        loaded: SecurityOfficer | None = self._run_loader("manager", self.manager_id)
        if loaded:
            self._manager = loaded

        return self._manager

    @manager.setter
    def manager(self, value: SecurityOfficer | None) -> None:
        self._manager = value
        if value and getattr(value, 'id', None) is not None:
            self.manager_id = value.id
        else:
            self.manager_id = None

    @property
    def subordinates(self) -> list[SecurityOfficer]:
        if self._subordinates is not None:
            return self._subordinates

        if self.id is not None:
            loaded: list[SecurityOfficer] | None = self._run_loader("subordinates", self.id)
            if loaded is not None:
                self._subordinates = loaded
                return self._subordinates

        self._subordinates = []
        return self._subordinates

    @property
    def incidents(self) -> list[Incident]:
        if self._incidents is not None:
            return self._incidents

        if self.incident_ids:
            loaded = self._run_loader("incidents", self.incident_ids)
            if loaded is not None:
                self._incidents = loaded
                return self._incidents

        self._incidents = []
        return self._incidents

    @incidents.setter
    def incidents(self, value: list[Incident]) -> None:
        self._incidents = value
        self.incident_ids = [inc.id for inc in value if inc.id is not None]


    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["terminal_id"] = self._get_fk_value(self._terminal, self.terminal_id)

        data["manager_id"] = self._get_fk_value(self._manager, self.manager_id)

        data["incident_ids"] = self._get_many_fk_value(self._incidents, self.incident_ids)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SecurityOfficer:
        instance = cast(SecurityOfficer, super().from_dict(data))

        cls._restore_fk(instance, data, "terminal_id", "terminal_id")

        cls._restore_fk(instance, data, "manager_id", "manager_id")

        cls._restore_many_fk(instance, data, "incident_ids", "incident_ids")

        return instance
