
"""FastAPI backend for the React expense dashboard.

The browser sends requests to these endpoints; this module validates the
requests, reads or updates the JSON files, and returns JSON responses.
"""

# from fastapi import FastAPI

# app = FastAPI(title="AI Expense Tracker API")


# @app.get("/")
# def home():
#     return {
#         "message": "Welcome to my AI Expense Tracker API"
#     }


# @app.get("/expenses")
# def get_expenses():
#     return {
#         "message": "This endpoint will return all expenses"
#     }

# from fastapi.middleware.cors import CORSMiddleware


# import json
# from pathlib import Path

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field

# app = FastAPI(title="AI Expense Tracker API")

# # CONNECTING FRONTEND TO BACKEND
# )

# # Locate expenses.json in the same folder as api.py
# DATA_FILE = Path(__file__).parent / "expenses.json"


# def load_expenses():
#     if not DATA_FILE.exists():
#         return []

#     with open(DATA_FILE, "r", encoding="utf-8") as file:
#         return json.load(file)


# def save_expenses(expenses):
#     with open(DATA_FILE, "w", encoding="utf-8") as file:
#         json.dump(expenses, file, indent=4)


# # Validate incoming expense data
# class Expense(BaseModel):
#     description: str = Field(min_length=1)
#     amount: float = Field(gt=0)
#     category: str = "Other"


# @app.get("/")
# def home():
#     return {"message": "AI Expense Tracker API is running!"}


# # Get all expenses
# @app.get("/expenses")
# def get_expenses():
#     return load_expenses()


# # Add an expense
# @app.post("/expenses")
# def add_expense(expense: Expense):
#     expenses = load_expenses()

#     next_id = max(
#         (item.get("id", 0) for item in expenses),
#         default=0
#     ) + 1

#     new_expense = {
#         "id": next_id,
#         **expense.model_dump()
#     }

#     expenses.append(new_expense)
#     save_expenses(expenses)

#     return new_expense


# # Get one expense
# @app.get("/expenses/{expense_id}")
# def get_expense(expense_id: int):
#     expenses = load_expenses()

#     for expense in expenses:
#         if expense.get("id") == expense_id:
#             return expense

#     raise HTTPException(
#         status_code=404,
#         detail="Expense not found"
#     )


# # Delete an expense
# @app.delete("/expenses/{expense_id}")
# def delete_expense(expense_id: int):
#     expenses = load_expenses()

#     updated_expenses = [
#         expense for expense in expenses
#         if expense.get("id") != expense_id
#     ]

#     if len(updated_expenses) == len(expenses):
#         raise HTTPException(
#             status_code=404,
#             detail="Expense not found"
#         )

#     save_expenses(updated_expenses)

#     return {"message": "Expense deleted successfully"}


# # Calculate total expenses
# @app.get("/summary")
# def expense_summary():
#     expenses = load_expenses()

#     total = sum(item["amount"] for item in expenses)

#     return {
#         "total_expenses": round(total, 2),
#         "number_of_expenses": len(expenses)
#     }


# @app.put("/expenses/{expense_id}")
# def update_expense(expense_id: int, updated_data: Expense):
#     expenses = load_expenses()

#     for index, expense in enumerate(expenses):
#         if expense.get("id") == expense_id:
#             updated_expense = {
#                 "id": expense_id,
#                 **updated_data.model_dump()
#             }

#             expenses[index] = updated_expense
#             save_expenses(expenses)

#             return updated_expense

#     raise HTTPException(
#         status_code=404,
#         detail="Expense not found"
#     )


from fastapi.middleware.cors import CORSMiddleware

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field, field_validator
from typing import Literal
from ai_categorizer import predict_category, train_model

from ai_categorizer import predict_category

app = FastAPI(title="PennyPilot API")


# Let the Vite development server call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Keep the app's data files beside this backend module, independent of the
# directory from which the API server is started.
DATA_FILE = Path(__file__).parent / "expenses.json"

CATEGORIES_FILE = Path(__file__).parent / "categories.json"
TRAINING_FILE = Path(__file__).parent / "training_data.json"


def load_expenses():
    """Read all expense records; a missing file represents an empty tracker."""
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_expenses(expenses):
    """Persist the complete expense list after a create, edit, or delete."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def load_json_file(file_path):
    """Read a JSON data file such as the category or training-example list."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json_file(file_path, data):
    """Write JSON data back to the file used by the corresponding API feature."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# These Pydantic models validate browser request bodies before route functions
# run, so invalid descriptions, amounts, or category inputs receive an API error.
# class Expense(BaseModel):
#     description: str = Field(min_length=1)
#     amount: float = Field(gt=0)
#     category: str = "Other"



class Expense(BaseModel):
    """Request shape for creating or replacing an expense record."""

    description: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str | None = None

    @field_validator("category", mode="before")
    @classmethod
    def categorize_expense(cls, value, info):
        """Predict a category only when the caller leaves it blank."""
        if value is None or value == "":
            description = info.data.get("description", "")
            if description:
                return predict_category(description)
            return "Other"
        return value

class CategoryInput(BaseModel):
    """Request shape for adding a category from the dashboard."""

    name: str = Field(min_length=1, max_length=50)


class TrainingExample(BaseModel):
    """A labeled description used to teach the category predictor."""

    description: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=1, max_length=50)


@app.get("/")
def home():
    """Simple health-check endpoint used to confirm that the API is running."""
    return {"message": "PennyPilot API is running!"}


# Expense routes form the data flow used by the dashboard's transaction list,
# summary cards, charts, and add/edit/delete actions.
@app.get("/expenses")
def get_expenses():
    """Return all saved expenses for the dashboard."""
    return load_expenses()


@app.post("/expenses")
def add_expense(expense: Expense):
    expenses = load_expenses()

    # Assign the next integer ID so the frontend can address this record later.
    next_id = max(
        (item.get("id", 0) for item in expenses),
        default=0
    ) + 1

    new_expense = {
        "id": next_id,
        **expense.model_dump()
    }

    expenses.append(new_expense)
    save_expenses(expenses)

    return new_expense


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    """Return one expense, or a 404 response if its ID is unknown."""
    expenses = load_expenses()

    for expense in expenses:
        if expense.get("id") == expense_id:
            return expense

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, updated_data: Expense):
    """Replace the matching record while keeping its existing ID."""
    expenses = load_expenses()

    for index, expense in enumerate(expenses):
        if expense.get("id") == expense_id:
            updated_expense = {
                "id": expense_id,
                **updated_data.model_dump()
            }

            expenses[index] = updated_expense
            save_expenses(expenses)

            return updated_expense

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    """Remove a record and report 404 when no record had the requested ID."""
    expenses = load_expenses()

    updated_expenses = [
        expense for expense in expenses
        if expense.get("id") != expense_id
    ]

    if len(updated_expenses) == len(expenses):
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    save_expenses(updated_expenses)

    return {"message": "Expense deleted successfully"}


@app.get("/summary")
def expense_summary():
    """Return aggregate expense values for clients that need a summary."""
    expenses = load_expenses()

    total = sum(item["amount"] for item in expenses)

    return {
        "total_expenses": round(total, 2),
        "number_of_expenses": len(expenses)
    }


@app.get("/categories")
def get_categories():
    """Supply the category choices used by the dashboard's category selector."""
    return load_json_file(CATEGORIES_FILE)


@app.post("/categories")
def add_category(category: CategoryInput):
    """Add a unique category to the list shared with the dashboard."""
    categories = load_json_file(CATEGORIES_FILE)

    name = category.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Category name cannot be empty."
        )

    if any(item.lower() == name.lower() for item in categories):
        raise HTTPException(
            status_code=409,
            detail="This category already exists."
        )

    categories.append(name)
    save_json_file(CATEGORIES_FILE, categories)

    return {"message": "Category added successfully", "category": name}


@app.post("/training-examples")
def add_training_example(example: TrainingExample):
    """Save a labeled example and rebuild the predictor from all saved examples."""
    categories = load_json_file(CATEGORIES_FILE)
    category = example.category.strip()
    description = example.description.strip()

    if not any(item.lower() == category.lower() for item in categories):
        raise HTTPException(
            status_code=400,
            detail="Create the category before adding examples."
        )

    data = load_json_file(TRAINING_FILE)

    data.append({
        "description": description,
        "category": category
    })

    save_json_file(TRAINING_FILE, data)

    try:
        count = train_model()
    except Exception:
        # Keep the training file consistent with the currently usable model if
        # the new example makes retraining impossible.
        data.pop()
        save_json_file(TRAINING_FILE, data)
        raise HTTPException(
            status_code=500,
            detail="Could not retrain the model."
        )

    return {
        "message": "Training example saved and model retrained.",
        "training_examples": count
    }
