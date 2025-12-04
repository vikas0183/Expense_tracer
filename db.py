"""
Database connection wrapper.
Using SQLite to keep things simple for local execution.
"""

import sqlite3

def get_connection():
    con = sqlite3.connect("expenses.db")
    con.row_factory = sqlite3.Row
    return con
