from src.byt_project.models.destination import Destination


class Route:
    def __init__(self, routed: str, destination_from: Destination, destination_to: Destination):
        self.routed = routed
        self.destination_from = destination_from
        self.destination_to = destination_to

        self.duration: float = 0.0
        self.distance: float = 0.0

        self.isInternational: bool = (
            destination_from.location.country != destination_to.location.country
        )

    def __repr__(self):
        inter = "International" if self.isInternational else "Domestic"
        return f"Route({self.routed}, {inter})"