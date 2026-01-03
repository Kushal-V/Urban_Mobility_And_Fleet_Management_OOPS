from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, vehicle_id, model, battery_percentage):
        self.vehicle_id = vehicle_id
        self.model = model
        self.battery_percentage = None
        self.__status = "Available"
        self.__maintenance_status = "Good"
        self.__rental_price = 0
        self.set_battery_percentage(battery_percentage)

    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return False
        return self.vehicle_id == other.vehicle_id

    def get_battery_percentage(self):
        return self.battery_percentage

    def set_battery_percentage(self, battery_percentage):
        if 0 <= battery_percentage <= 100:
            self.battery_percentage = battery_percentage
        else:
            print("Battery percentage must be between 0 and 100")

    def get_maintenance_status(self):
        return self.__maintenance_status

    def set_maintenance_status(self, maintenance_status):
        self.__maintenance_status = maintenance_status

    def get_rental_price(self):
        return self.__rental_price

    def set_rental_price(self, rental_price):
        if rental_price > 0:
            self.__rental_price = rental_price
        else:
            print("Invalid rental price")

    def get_status(self):
        return self.__status
    
    def set_status(self,status):
        if status in ["Available", "On Trip", "Under Maintenance"]:
            self.__status = status
        else:
            print("Invalid status")

    @abstractmethod
    def calculate_trip_cost(self, distance):
        pass
