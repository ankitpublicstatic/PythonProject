# MySQL connection demo
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost",user="root",password="password",database="testdb")
    print("Connected to", conn.database)
    conn.close()
except mysql.connector.Error as e:
    print("Error:", e)
