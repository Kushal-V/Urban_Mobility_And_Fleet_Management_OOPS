from electric_car import ElectricCar
from electric_scooter import ElectricScooter
import csv
import json

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

    def fleet_analysis(self):
        fleet_vehicles = {
            'Available': 0,
            'On Trip' : 0,
            'Under Maintenance' : 0
        }

        for hub in self.hubs.values():
            for vehicle in hub:
                status = vehicle.get_status()
                # Ensure status is one of the expected keys to avoid KeyError if data is corrupted
                if status in fleet_vehicles:
                    fleet_vehicles[status] += 1
                else:
                    # Optional: handle unexpected status
                    pass

        print("\nFleet Analysis:")
        for status, count in fleet_vehicles.items():
            print(f"{status}: {count}")

    def sort_vehicles(self):
        for vehicles in self.hubs.values():
            vehicles.sort(key=lambda v: v.model.lower())
        
        for hub, vehicles in self.hubs.items():
            print(f"\nHub: {hub}")
            for v in vehicles:
                print(f"- {v}")

    def advanced_sorting(self):
        sort_type = input("Enter sorting type (battery-level or fare-price): ").lower()

        all_vehicles = [
            v for hub in self.hubs.values() for v in hub
        ]

        if sort_type == "battery-level":
            # Sort by battery descending
            sorted_vehicles = sorted(all_vehicles, key=lambda v: v.get_battery_percentage(), reverse=True)
            for v in sorted_vehicles:
                print(f"{v} Battery: {v.get_battery_percentage()}")
            
        elif sort_type == "fare-price":
            def fare_price(v):
                # Standardize trip for comparison: 10km for cars, 30min for scooters
                if isinstance(v, ElectricCar):
                    return v.calculate_trip_cost(10)
                elif isinstance(v, ElectricScooter):
                    return v.calculate_trip_cost(30)
                else:
                    return float('inf')
            
            sorted_vehicles = sorted(all_vehicles, key=fare_price)
            for v in sorted_vehicles:
                print(f"{v} Fare: {fare_price(v)}")
            
        else:
            print("Invalid sorting type")

    def save_data_to_csv(self):
        file_path = input("Enter file path: ")

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Hub", "VehicleType", "VehicleID", "Model",
                "Battery", "Status",
                "MaintenanceStatus", "RentalPrice",
                "SeatingCapacity", "MaxSpeed"
            ])

            for hub, vehicles in self.hubs.items():
                for v in vehicles:
                    if isinstance(v, ElectricCar):
                        writer.writerow([
                            hub, "ElectricCar", v.vehicle_id, v.model,
                            v.get_battery_percentage(), v.get_status(),
                            v.get_maintenance_status(), v.get_rental_price(),
                            v.seating_capacity, ""
                        ])
                    elif isinstance(v, ElectricScooter):
                        writer.writerow([
                            hub, "ElectricScooter", v.vehicle_id, v.model,
                            v.get_battery_percentage(), v.get_status(),
                            v.get_maintenance_status(), v.get_rental_price(),
                            "", v.max_speed_limit
                        ])
        print("Data saved successfully")

    def load_data_from_csv(self):
        file_path = input("Enter file path: ")
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                self.hubs.clear()
                for row in reader:
                    hub = row["Hub"]
                    if hub not in self.hubs:
                        self.hubs[hub] = []
                    
                    if row["VehicleType"] == "ElectricCar":
                        vehicle = ElectricCar(
                            row["VehicleID"],
                            row["Model"],
                            int(row["Battery"]),
                            int(row["SeatingCapacity"])
                        )
                    elif row["VehicleType"] == "ElectricScooter":
                        vehicle = ElectricScooter(
                            row["VehicleID"],
                            row["Model"],
                            int(row["Battery"]),
                            int(row["MaxSpeed"])
                        )
                    vehicle.set_status(row["Status"])
                    vehicle.set_maintenance_status(row["MaintenanceStatus"])
                    vehicle.set_rental_price(float(row["RentalPrice"]))
                    self.hubs[hub].append(vehicle)   
            print("Data loaded successfully")
        
        except FileNotFoundError:
            print("File not found")

    def save_data_to_json(self):
        file_path = input("Enter file path: ")
        data = {}
        for hub, vehicles in self.hubs.items():
            data[hub] = [v.to_json() for v in vehicles]
        
        with open(file_path,'w') as file:
            json.dump(data, file, indent=4)
        print("Data saved successfully")
        
    
    def load_data_from_json(self):
        file_path = input("Enter file path: ")
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
            self.hubs.clear()

            for hub, vehicles in data.items():
                self.hubs[hub] = []

                for v in vehicles:
                    if v["vehicle_type"] == "ElectricCar":
                        vehicle = ElectricCar(
                            v["vehicle_id"],
                            v["model"],
                            int(v["battery"]),
                            int(v["seating_capacity"])
                        )
                    elif v["vehicle_type"] == "ElectricScooter":
                        vehicle = ElectricScooter(
                            v["vehicle_id"],
                            v["model"],
                            int(v["battery"]),
                            int(v["max_speed_limit"])
                        )
                    vehicle.set_status(v["status"])
                    vehicle.set_maintenance_status(v["maintenance_status"])
                    vehicle.set_rental_price(v["rental_price"])
                    self.hubs[hub].append(vehicle)
            print("Data loaded successfully")
            
        except FileNotFoundError:
            print("File not found")
