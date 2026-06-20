# fk_check.py

import sqlite3

conn = sqlite3.connect(
    "nifty100.db"
)

cursor = conn.cursor()

cursor.execute(
    "PRAGMA foreign_key_check;"
)

errors = cursor.fetchall()

if len(errors) == 0:

    print(
        "No foreign key violations found."
    )

else:

    print(
        "Foreign key violations:"
    )

    for err in errors:
        print(err)

conn.close()