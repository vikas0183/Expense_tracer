"""Simple CLI based expense calculator
   this file is the base model, which provide the choices and take input.
   Based on the user choice it calls the respective function.
"""
from models import init_db
from services import ExpenseService

def main():
    # Creating Tables
    init_db()

    service = ExpenseService()

    MENU = """
_____________________________
 Expense Tracker - Main Menu
_____________________________
1. Add an Expense
2. Set Monthly Budget
3. View Summary Report
4. Exit
_____________________________
"""

    while True:
        print(MENU)
        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category (Food/Transport/Entertainment/etc): ")
            service.add_expense(amount, category)
            print(" Expense added to "+category+".\n")

        elif choice == "2":
            month = input("Month (e.g 2025-12): ")
            category = input("Category: ")
            budget = float(input("Budget amount: "))
            service.set_budget(month, category, budget)
            print("Budget saved for "+category+".\n")

        elif choice == "3":
            month = input("Month to view (YYYY-MM): ")
            service.generate_report(month)

        elif choice == "4":
            print("Come again to add furthur expences")
            break

        else:
            print("Invalid choice. please try again.\n")

if __name__ == "__main__":
    main()
