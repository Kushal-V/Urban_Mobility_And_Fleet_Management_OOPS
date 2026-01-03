from electric_car import ElectricCar
from electric_scooter import ElectricScooter

class FleetManager:
    def __init__(self):
        self.hubs = {}

    def add_hub(self):
        hub_name = input("Enter hub name: ")
        if hub_name in self.hubs:
            print("Hub already exists")
        else:
            self.hubs[hub_name] = []
            print(f"Hub '{hub_name}' added successfully")

    def add_vehicle(self):
        hub_name = input("Enter hub name: ")
        if hub_name not in self.hubs:
            print("Hub does not exist")
            return

        vehicle_type = input("Enter vehicle type (car/scooter): ").lower()
        vehicle_id = input("Enter vehicle ID: ")

        existed_vehicle = [
            v for v in self.hubs[hub_name] if v.vehicle_id == vehicle_id
        ]

        if existed_vehicle:
            print("Vehicle already exists")
            return

        model = input("Enter model: ")
        try:
            battery = int(input("Enter battery percentage: "))
        except ValueError:
            print("Invalid battery percentage")
            return

        if vehicle_type == "car":
            try:
                seats = int(input("Enter seating capacity: "))
                vehicle = ElectricCar(vehicle_id, model, battery, seats)
            except ValueError:
                print("Invalid seating capacity")
                return

        elif vehicle_type == "scooter":
            try:
                speed = int(input("Enter max speed limit: "))
                vehicle = ElectricScooter(vehicle_id, model, battery, speed)
            except ValueError:
                print("Invalid speed limit")
                return

        else:
            print("Invalid vehicle type")
            return

        self.hubs[hub_name].append(vehicle)
        print("Vehicle added successfully")