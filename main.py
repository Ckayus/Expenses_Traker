
"""Standalone terminal version of the expense tracker.

This older command-line flow reads and writes ``expenses.json`` directly. It
does not call ``api.py``; the React dashboard instead uses the FastAPI routes.
"""

import os
import json
from datetime import datetime

# The CLI keeps its current records in memory between loading and saving.
expenses = []

# ==============================
# LOAD EXPENSES
# ==============================
def load_expenses():
    """Populate the in-memory list from the JSON file, or start empty."""
    global expenses

    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
            #return json.load(file)

    except FileNotFoundError:
        expenses = []

    except json.JSONDecodeError:
        print("Warning: expenses.json is corrupted.")
        expenses = []


# ==============================
# ADD EXPENSE
# ==============================
def add_expense():
    """Prompt for a new record, append it, then persist the updated list."""
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
    """Sum the amounts currently held in the in-memory expense list."""
    total = 0

    for expense in expenses:
        total += float(expense["amount"])

    return total


# ==============================
# VIEW EXPENSES
# ==============================
def view_expenses():
    """Print every record in a table followed by the overall total."""
    if not expenses:
        print("No Expenses is found.")
        return
    print("\n========== ALL EXPENSES ==========")

    if len(expenses) == 0:
        print("No expenses found.")
        return

    print(
        f"{'No.:':<5}"
        f"{'Date':<13}"
        f"{'Category':<12}"
        f"{'Description':<17}"
        f"{'Amount':>5}"
    )

    print("-" * 58)

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<5}"
            f"{expense['date']:<13}"
            f"{expense['category']:<12}"
            f"{expense['description']:<17}"
            f"₦{expense['amount']:<5,.2f}"
        )

    print("-" * 58)

    total = calculate_total()

    print(f"{'Total Expenses:':<45} ₦{total:<5,.2f}")


def search_expenses():
    """Print records whose category matches the user's search, ignoring case."""
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
    """Remove the selected record from memory using its displayed list number."""
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
    """Write the in-memory list to the CLI's JSON data file."""
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)



# ==============================
# EDIT EXPENSE
# ==============================
def edit_expense():
    """Prompt for replacement values and save them to the selected record."""
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

    #===================================
    #       SORTED BY AMOUNT
    #===================================

def sort_by_amount():
    """Display a separate, highest-to-lowest view without reordering saved data."""
    if not expenses:
        print("No expenses to sort.")
        return

    sorted_expenses = sorted(
        expenses,
        key=lambda expense: float(expense["amount"]),
        reverse = True

    )

    print("\n============ EXPENSES SORTED BY AMOUNT =========")

    for index, expense in enumerate (sorted_expenses, start=1):
        print(
            f"{index:<5}"
            f"{expense['description']:<20}"
            f"₦{expense['amount']:<10}"
        )


#===================================
#       MONTHLY SUMMARY.
#===================================
        
def monthly_summary():
    """Group displayed totals using the first seven characters of each date."""
    if not expenses:
        print("No expenses available")
        return

    monthly_totals = {}

    for expense in expenses:
        month = expense["date"][:7]

        if month not in monthly_totals:
            monthly_totals[month] = 0

        monthly_totals[month] += expense["amount"]

    print("\n=============MONHLY SUMMARY============")

    for month, total in sorted(monthly_totals.items()):
        print(f"{month:<10} ₦{total:>15}")


# ==============================
# PAUSE FUNCTION
# ==============================

def pause():
    """Wait for Enter so the user can read output before the screen is cleared."""
    input("\n Press Enter to continue")


# ==============================
# CLEAR SCREEN FUNCTION
# ==============================

def clear_screen():
    """Use the appropriate terminal clear command for the current OS."""
    os.system("cls" if os.name == "nt" else "clear")

# ==============================
# MAIN PROGRAM
# ==============================

# Startup loads the file and shows existing records before entering the menu.
load_expenses()
pause()

view_expenses()
pause()

while True:

    # Each menu choice delegates to one of the operations above; those
    # operations update the in-memory list and save it when needed.
    clear_screen()

    print("\n====================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("====================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total")
    print("4. Search Expenses")
    print("5. Delete Expense")
    print("6. Edit Expense")
    print("7. Monthly Summary")
    print("8. Sort Expenses by Amount")
    print("9. Exit")
    print("====================================")

    choice = input("Enter your choice: ")

    if choice == "1":

        add_expense()
        pause()

    elif choice == "2":

        view_expenses()
        pause()

    elif choice == "3":

        total = calculate_total()

        print(f"\nTotal Expenses = ₦{total:,.2f}")
        pause()

    elif choice == "4":
        search_expenses()
        pause()


    elif choice == "5":
        delete_expense()
        pause()

    elif choice == "6":
        edit_expense()
        pause()

    elif choice == "7":
        monthly_summary()
        pause()

    elif choice == "8":
        sort_by_amount()
        pause()

    elif choice == "9":

        print("\nThank you for using PennyPilot!")
        break

    else:

        print("\nInvalid choice. Please enter 1, 2, 3, or 4.")