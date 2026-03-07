import mysql.connector
import time

def connect_sql(root_password, database_name):
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password=root_password,
                database=database_name
            )
            print("Connected to MySQL database successfully")
            return conn
        except Exception as e:
            print(f"Failed to connect to MySQL database: {e}")
            time.sleep(2)  # Wait 5 seconds before retrying

    raise Exception("Failed to connect to MySQL database after 10 attempts")