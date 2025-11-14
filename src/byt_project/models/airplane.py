from datetime import datetime


class Airplane:
    maxServiceYears = 30

    def __init__(
        self,
        model: str,
        manufacturer: str,
        capacity: int,
        max_luggage_weight: float,
        year_of_manufacture: int,
        airline: Airline
    ):
        self.model = model
        self.manufacturer = manufacturer
        self.capacity = capacity
        self.maxLuggageWeight = max_luggage_weight
        self.yearOfManufacture = year_of_manufacture
        self.airline = airline



    def yearsInService(self) -> int:
        current_year = datetime.now().year
        return current_year - self.yearOfManufacture

    def isExpired(self) -> bool:
        return self.yearsInService() > Airplane.maxServiceYears