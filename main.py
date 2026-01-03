from fleet_manager import FleetManager

manager = FleetManager()

while True:
    print("\nMenu:")
    print("1. Add hub")
    print("2. Add vehicle")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        manager.add_hub()
    elif choice == "2":
        manager.add_vehicle()
    elif choice == "3":
        break
    else:
        print("Invalid choice")