import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='ticketsystem',
            auth_plugin='mysql_native_password'
        )
        print("Connected to MySQL database")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None
def close_database_connection(conn):
    if conn:
        conn.close()
        print("Database connection closed")
