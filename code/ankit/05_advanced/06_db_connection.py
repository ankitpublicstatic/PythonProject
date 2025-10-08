
# Database connection demo (MySQL)
# Requires: pip install mysql-connector-python

import mysql.connector

def main():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",        # change to your MySQL username
            password="password",# change to your MySQL password
            database="testdb"   # ensure this DB exists
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        print("Connected to database:", cursor.fetchone())
        conn.close()
    except mysql.connector.Error as e:
        print("Database error:", e)

if __name__ == "__main__":
    main()