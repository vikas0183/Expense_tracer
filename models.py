# models.py
"""
In this file, database for the expenses tracker is created.
Runs automatically when we run the app.py file
"""

from db import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # expenses table
    cur.execute("""
        create table if not exists expenses (
            id integer primary key autoincrement,
            amount float not null,
            category varchar(30) not null,
            created_at varchar(30) not null
        )
    """)
    # budget table
    cur.execute("""
        create table if not exists budgets (
            id integer primary key autoincrement,
            month varchar(10) not null,
            category varchar(30) not null,
            budget float not null,
            unique(month, category)
        )
    """)

    conn.commit()
    conn.close()

# initialization
init_db()
