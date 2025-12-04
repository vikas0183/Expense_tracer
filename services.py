# services.py
"""
logic for handling expenses, budgets, alerts, and reports.
"""

from db import get_connection
from datetime import datetime


class ExpenseService:

    # Add an Expense + Instant Alerts
    
    def add_expense(self, amount: float, category: str):
        conn = get_connection()
        cur = conn.cursor()

        # Insert the new expense code
        cur.execute("""
            INSERT INTO expenses (amount, category, created_at)
            VALUES (?, ?, ?)
        """, (amount, category, datetime.now().isoformat()))
        conn.commit()

        #  INSTANT ALERT LOGIC code
        now_month = datetime.now().strftime("%Y-%m")

        # Total spent in this category for the current month code
        cur.execute("""
            SELECT SUM(amount) AS spent
            FROM expenses
            WHERE category = ? AND substr(created_at, 1, 7) = ?
        """, (category, now_month))
        spent_row = cur.fetchone()
        total_spent = spent_row["spent"] or 0

        # To Fetch  the budget for this category/month code
        cur.execute("""
            SELECT budget FROM budgets
            WHERE month = ? AND category = ?
        """, (now_month, category))
        budget_row = cur.fetchone()

        if budget_row:
            budget = budget_row["budget"]

            if total_spent > budget:
                print(f"\n ALERT: Budget exceeded for '{category}'!")
                print(f"Spent: {total_spent:.2f} | Budget: {budget:.2f}\n")

            elif total_spent >= 0.9 * budget:
                print(f"\n Warning: You have used more than 90% of your '{category}' budget")
                print(f"Spent: {total_spent:.2f} | Budget: {budget:.2f}\n")

        conn.close()

    # Set Category Budget Code
    
    def set_budget(self, month: str, category: str, budget: float):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO budgets (month, category, budget)
            VALUES (?, ?, ?)
            ON CONFLICT(month, category)
            DO UPDATE SET budget = excluded.budget
        """, (month, category, budget))

        conn.commit()
        conn.close()

    # Generate Monthly Summary Report
    
    def generate_report(self, month: str):
        conn = get_connection()
        cur = conn.cursor()

        print(f"\n==== Summary Report for {month} ===")

        # Total monthly spending
        cur.execute("""
            SELECT SUM(amount) AS total
            FROM expenses
            WHERE substr(created_at, 1, 7) = ?
        """, (month,))
        total_row = cur.fetchone()
        total_spent = total_row["total"] or 0
        print(f"Total Spending: ₹{total_spent:.2f}\n")

        # Category-wise spending
        cur.execute("""
            SELECT category, SUM(amount) AS spent
            FROM expenses
            WHERE substr(created_at, 1, 7) = ?
            GROUP BY category
        """, (month,))
        rows = cur.fetchall()

        for row in rows:
            category = row["category"]
            spent = row["spent"]

            # Fetch budget for each category
            cur.execute("""
                SELECT budget FROM budgets
                WHERE month = ? AND category = ?
            """, (month, category))
            budget_row = cur.fetchone()
            budget = budget_row["budget"] if budget_row else 0

            # Decide status based on budjet used
            if budget == 0:
                status = "No Budget"
            elif spent > budget:
                status = " EXCEEDED"
            elif spent >= 0.9 * budget:
                status = "Near Limit"
            else:
                status = "OK"

            print(f"{category}: Spent {spent:.2f} / Budget {budget:.2f} → {status}")

        print("====================\n")

        conn.close()
