from vehicle import Vehicle

class ElectricScooter(Vehicle):
    def __init__(self, vehicle_id, model, battery_percentage, max_speed_limit):
        super().__init__(vehicle_id, model, battery_percentage)
        self.max_speed_limit = max_speed_limit

    def calculate_trip_cost(self, distance):
        # For scooter, we assume 'distance' represents minutes for simplicity in polymorphic calls
        return 1.00 + (distance * 0.15)