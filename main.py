import json
from datetime import datetime

# Store all expenses here
expenses = []


# ==============================
# ADD EXPENSE
# ==============================
def add_expense():
    print("\n========== ADD EXPENSE ==========")

    date = datetime.now().strftime("%d-%m-%Y")

    category = input("Enter category (e.g. Food, Transport, Gifts): ")
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: ₦"))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(expense)

    # Save immediately after adding
    save_expenses()

    print("\nExpense added successfully!")


# ==============================
# CALCULATE TOTAL
# ==============================
def calculate_total():
    total = 0

    for expense in expenses:
        total += float(expense["amount"])

    return total


# ==============================
# VIEW EXPENSES
# ==============================
def view_expenses():
    print("\n========== ALL EXPENSES ==========")

    if len(expenses) == 0:
        print("No expenses found.")
        return

    print(
        f"{'Date':<15}"
        f"{'Category':<15}"
        f"{'Description':<20}"
        f"{'Amount':>15}"
    )

    print("-" * 65)

    for expense in expenses:
        print(
            f"{expense['date']:<15}"
            f"{expense['category']:<15}"
            f"{expense['description']:<20}"
            f"₦{expense['amount']:>14,.2f}"
        )

    print("-" * 65)

    total = calculate_total()

    print(f"{'Total Expenses:':<50} ₦{total:,.2f}")


def search_expenses():
    search_category = input("Enter category: ")

    found = False

    for expense in expenses:
        if expense["category"].lower() == search_category.lower():
            print(f"Description: {expense['description']}")
            print(f"Amount: #{expense['amount']:,.2f}")
            print("_" * 30)

            found = True

    if not found:
        print("No expenses found in that category")

def delete_expense():
    if not expenses:
        print("There are no expenses to delete.")
        return

    print("\n========== DELETE EXPENSE ==========")

    for index, expense in enumerate(expenses, start=1):
        print(f"{index}. {expense['description']}")

    choice = input("Which expense do you want to delete? ")

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(expenses):
        print("Invalid expense number.")
        return

    deleted_expense = expenses.pop(choice - 1)

    print(f"{deleted_expense['description']} deleted successfully.")


# ==============================
# SAVE EXPENSES
# ==============================
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


# ==============================
# LOAD EXPENSES
# ==============================
def load_expenses():
    global expenses

    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)

    except FileNotFoundError:
        expenses = []

    except json.JSONDecodeError:
        print("Warning: expenses.json is corrupted.")
        expenses = []

# ==============================
# EDIT EXPENSE
# ==============================
def edit_expense():
    if not expenses:
        print("There are no expenses to edit.")
        return

    print("\n========== EDIT EXPENSE ==========")

    # Display all expenses with an index
    for index, expense in enumerate(expenses, start=1):
        print(f"{index}. [{expense['date']}] {expense['category']} - {expense['description']}: ₦{expense['amount']:,.2f}")

    choice = input("\nWhich expense do you want to edit? ")

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(expenses):
        print("Invalid expense number.")
        return

    target_expense = expenses[index]

    print(f"\nEditing: {target_expense['description']}")

    # Get new inputs (press Enter to keep old values optionally, or require new values)
    category = input("Enter new category: ")
    description = input("Enter new description: ")

    try:
        amount = float(input("Enter new amount: ₦"))
    except ValueError:
        print("Invalid amount. Edit cancelled.")
        return

    # Update the dictionary values
    target_expense["category"] = category
    target_expense["description"] = description
    target_expense["amount"] = amount

    # Save changes immediately
    save_expenses()

    print("\nExpense updated successfully!")


# ==============================
# MAIN PROGRAM
# ==============================

load_expenses()

while True:

    print("\n====================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("====================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total")
    print("4. Search Expenses")
    print("5. Delete Expense")
    print("6. Edit Expense")
    print("7. Exit")
    print("====================================")

    choice = input("Enter your choice: ")

    if choice == "1":

        add_expense()

    elif choice == "2":

        view_expenses()

    elif choice == "3":

        total = calculate_total()

        print(f"\nTotal Expenses = ₦{total:,.2f}")

    elif choice == "4":
        search_expenses()

    elif choice == "5":
        delete_expense()

    elif choice == "6":
        edit_expense()

    elif choice == "7":

        print("\nThank you for using the Expense Tracker!")
        break

    else:

        print("\nInvalid choice. Please enter 1, 2, 3, or 4.")