from src.byt_project.models.incident import Incident
from src.byt_project.repositories import BaseRepository


class IncidentRepository(BaseRepository[Incident]):
    def __init__(self) -> None:
        super().__init__(model_cls=Incident)

    def find_all_by_security_officer_id(self, security_officer_id: int) -> list[Incident]:
        pass
