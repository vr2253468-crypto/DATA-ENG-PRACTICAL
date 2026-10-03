import sqlite3

conn = sqlite3.connect("data/app.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    salary REAL
);
""")


cursor.execute("DELETE FROM users")  
cursor.executemany("INSERT INTO users (name, salary) VALUES (?, ?)", [
    ("Alice", 75000),
    ("Bob", 50000),
    ("Charlie", 90000)
])
conn.commit()
print("[CREATE] Seeded 3 records.")


print("\n--- [READ] Users Table ---")
for row in cursor.execute("SELECT * FROM users").fetchall():
    print(f"ID: {row['id']} | Name: {row['name']:<10} | Salary: ${row['salary']:,.2f}")


cursor.execute("UPDATE users SET salary = ? WHERE name = ?", (82000, "Bob"))
conn.commit()
print("\n[UPDATE] Updated Bob's salary to $82,000.")


cursor.execute("DELETE FROM users WHERE name = ?", ("Charlie",))
conn.commit()
print("[DELETE] Deleted Charlie.")


print("\n--- Final Records ---")
for row in cursor.execute("SELECT * FROM users").fetchall():
    print(f"ID: {row['id']} | Name: {row['name']:<10} | Salary: ${row['salary']:,.2f}")

conn.close()