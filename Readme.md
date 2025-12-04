# Expense Tracker (Python CLI)

A simple Python-based backend application to track expenses, categorize them,
set budgets, and generate monthly spending reports.

# How to Run

1. Create virtual environment:
    python -m venv venv
    source venv/bin/activate


3. Run the app:
    python app.py

The application will automatically create a SQLite database file: expenses.db.

---

## How to use the app.

- First create a budget for a category using choise 2
- Try to add the expense for that category using choice 1
- Add expenses more than the budget to check the alert (budget overriding).
- Run report after many categories using choise 3
- Exit the app using exit choice

---

## Docker Instruction

### Build
docker build -t expense-tracker .

### Run
docker run -it expense-tracker

