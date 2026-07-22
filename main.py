
while True:
    print("\n==========================================")
    print("PERSONAL EXPENSES TRACKER")
    print("==========================================")

    print("1. Add Expenses")
    print("2. View Expenses")
    print("3. Exit")

    choice = input("enter your choice:")
    name = input("Enter your name:")

    if choice == "1":
        print ("You selected Add Expenses")
    elif choice == "2":
        print("You selected View Expenses")
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice.")