# MySQL DB connection demo
# Requires: pip install mysql-connector-python
import mysql.connector

try:
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testdb"
    )
    print("Connected to database:", conn.database)
    conn.close()
except mysql.connector.Error as e:
    print("Database error:",e)
