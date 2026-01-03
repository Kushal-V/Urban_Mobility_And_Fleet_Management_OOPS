from vehicle import Vehicle

class ElectricCar(Vehicle):
    def __init__(self, vehicle_id, model, battery_percentage, seating_capacity):
        super().__init__(vehicle_id, model, battery_percentage)
        self.seating_capacity = seating_capacity

    def calculate_trip_cost(self, distance):
        return 5.00 + (distance * 0.50)