
"""Text-based expense categorization used by the FastAPI expense endpoint.

The API calls ``predict_category`` when an expense request has no category.
The model is trained from ``training_data.json`` and can be retrained after a
new labeled example is added through the API.
"""

import json
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Small self-contained prototype kept for direct script demonstrations.
# The API uses the JSON-backed training workflow defined below instead.
# The parallel descriptions/categories entries are the prototype's labels.
descriptions = [
    "bought rice and beans",
    "bought groceries and food",
    "paid for lunch",
    "bought bread and milk",
    "paid for a bus ride",
    "bought petrol for my car",
    "paid for a taxi",
    "paid transport fare",
    "paid electricity bill",
    "paid water bill",
    "paid monthly internet subscription",
    "bought new shoes",
    "bought clothes",
    "purchased a new bag",
    "Paid for my house",
    "paid for my shop or office space",
]

categories = [
    "Food", "Food", "Food", "Food",
    "Transport", "Transport", "Transport", "Transport",
    "Bills", "Bills", "Bills",
    "Shopping", "Shopping", "Shopping",
    "Rent", "Rent"
]

# Convert each example into a bag-of-words feature vector for the prototype.
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(descriptions)

# Train a Naive Bayes classifier to map those word counts to category labels.
model = MultinomialNB()
model.fit(X, categories)


def predict_category(description):
    """Predict a category using the standalone in-file example model."""
    text = vectorizer.transform([description])
    return model.predict(text)[0]


# Running this file prints sample predictions from the prototype model.
if __name__ == "__main__":
    test_expenses = [
        "bought rice",
        "paid for petrol",
        "electricity payment",
        "purchased a shirt",
    ]

    for expense in test_expenses:
        category = predict_category(expense)
        print(f"{expense} -> {category}")





# The API-backed model reads editable examples from this JSON file.
BASE_DIR = Path(__file__).parent
TRAINING_FILE = BASE_DIR / "training_data.json"

# The API-backed vectorizer and classifier are replaced whenever train_model()
# reloads the training examples and fits a fresh model.
vectorizer = None
model = None


def load_training_data():
    """Load non-empty description/category pairs from the training file."""
    with open(TRAINING_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Ignore examples with empty descriptions or categories.
    return [
        item for item in data
        if item.get("description", "").strip()
        and item.get("category", "").strip()
    ]


def train_model():
    """Fit the API's classifier and vectorizer from all saved examples."""
    global vectorizer, model

    data = load_training_data()

    if not data:
        raise ValueError("No training examples found.")

    descriptions = [item["description"] for item in data]
    categories = [item["category"] for item in data]

    if len(set(categories)) < 2:
        raise ValueError(
            "Training requires examples from at least two categories."
        )

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(descriptions)

    model = MultinomialNB()
    model.fit(X, categories)

    return len(data)


def predict_category(description):
    """Predict an expense category using the JSON-backed model."""
    if model is None or vectorizer is None:
        train_model()

    text = vectorizer.transform([description])
    return model.predict(text)[0]


# Initialize the API-backed model on import so its first prediction is ready.
train_model()


if __name__ == "__main__":
    # This second sample demonstrates predictions from the JSON-backed model.
    examples = [
        "bought rice",
        "paid for petrol",
        "electricity payment",
        "purchased a shirt",
    ]

    for description in examples:
        print(f"{description} -> {predict_category(description)}")
