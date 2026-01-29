# MySQL connection demo
import mysql.connector
conn = None
try:
    conn = mysql.connector.connect(
        host="localhost",user="root",password="password",database="testdb")
    print("Connected to", conn.database)
    # conn.close()
except mysql.connector.Error as e:
    print("Error:", e)
finally:
    conn.close()
