
class Location:
    def __init__(self, country: str, city: str, latitude: float, longitude: float):
        self.country = country
        self.city = city
        self.latitude = latitude
        self.longitude = longitude


class Destination:
    def __init__(self, name: str, location: Location, airport: str):
        self.name = name
        self.location = location
        self.airport = airport