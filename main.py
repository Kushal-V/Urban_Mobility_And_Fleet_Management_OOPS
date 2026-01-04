from fleet_manager import FleetManager

manager = FleetManager()

while True:
    print("\nMenu:")
    print("1. Add hub")
    print("2. Add vehicle")
    print("3. Search vehicle")
    print("4. See vehicles by type")
    print("5. Fleet analysis")
    print("6. Sort vehicles")
    print("7. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        manager.add_hub()
    elif choice == "2":
        manager.add_vehicle()
    elif choice == "3":
        manager.search_vehicle()
    elif choice == "4":
        manager.search_vehicle_by_type()
    elif choice == "5":
        manager.fleet_analysis()
    elif choice == "6":
        manager.sort_vehicles()
    elif choice == "7":
        break
    else:
        print("Invalid choice")
