import json
from datetime import datetime

# Store all expenses here
expenses = []


# Function to add an expense
def add_expense():
    date = datetime.now().strftime("%d-%m-%Y")

    category = input("Enter category (e.g. Food, Transport, Gifts): ")
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(expense)

    print("\nExpense added successfully!")


# Function to view all expenses
def view_expenses():
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\nDate            Category        Description         Amount")
    print("---------------------------------------------------------------")

    for expense in expenses:
        print(
            f"{expense['date']:<15}"
            f"{expense['category']:<16}"
            f"{expense['description']:<20}"
            f"₦{expense['amount']:,.2f}"
        )

def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

    print("\nExpenses saved successfully!")

def load_expenses():
    global expenses

    try:
        with open ("expenses.json", "r") as file:
            expenses = json.load(file)

    except FileNotFoundError:
        expenses = []

# Main program
load_expenses()

while True:
    print("\n====================================")
    print("      PERSONAL EXPENSE TRACKER")
    print("====================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()
        save_expenses()
        print("Expenses added successfully!")

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        print("Thank you for using the Expense Tracker!")
        break

    else:
        print("Invalid choice. Please try again.")