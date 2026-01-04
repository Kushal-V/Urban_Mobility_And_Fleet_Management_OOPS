from vehicle import Vehicle

class ElectricCar(Vehicle):
    def __init__(self, vehicle_id, model, battery_percentage, seating_capacity):
        super().__init__(vehicle_id, model, battery_percentage)
    def calculate_trip_cost(self, distance):
        return 5.00 + (distance * 0.50)

    def to_json(self):
        data = super().to_json()
        data["seating_capacity"] = self.seating_capacity
        return data
