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

        # Check for duplicates in the specific hub (Basic check for now, UC 7 will improve this)
        existed_vehicle = [
            v for v in self.hubs[hub_name] if v.vehicle_id == vehicle_id
        ]

        if existed_vehicle:
            print("Vehicle already exists")
            return

        model = input("Enter model: ")
        # Input validation for battery could be added here or relied on class setter
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

    def search_vehicle(self):
        search_key = input("Enter hub location or 'battery' to search by battery > 80: ").lower()

        if search_key in self.hubs:
            print(f"\nVehicles in hub '{search_key}':")
            for v in self.hubs[search_key]:
                # Assuming simple print for now, __str__ will be improved in UC 11
                print(f"- {v.vehicle_id} ({v.model}, Battery: {v.get_battery_percentage()})")
            return

        elif search_key == "battery":
            print("\nVehicles with battery > 80:")
            all_vehicles = [
                v for hub in self.hubs.values() for v in hub
            ]

            high_battery_vehicles = list(
                filter(
                    lambda v: v.get_battery_percentage() > 80, all_vehicles
                )
            )

            if high_battery_vehicles:
                for v in high_battery_vehicles:
                    print(f"- {v.vehicle_id} ({v.model}, Battery: {v.get_battery_percentage()})")
            else:
                print("No vehicles found with battery > 80")
        
        else:
            print("Invalid search option")

    def search_vehicle_by_type(self):
        categorized = {}

        for hub in self.hubs.values():
            for vehicle in hub:
                vehicle_type = vehicle.get_type()
                if vehicle_type not in categorized:
                    categorized[vehicle_type] = []
                categorized[vehicle_type].append(vehicle)
        
        for vehicle_type, vehicles in categorized.items():
            print(f"\n{vehicle_type}s:")
            if vehicles:
                for v in vehicles:
                    print(f"- {v.vehicle_id} ({v.model}, Battery: {v.get_battery_percentage()})")
            else:
                print(f"No {vehicle_type}s found")
