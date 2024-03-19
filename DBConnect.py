import mysql.connector
def connect_to_database():
    try:
        # Replace 'hostname', 'username', 'password', and 'database' with your MySQL connection details
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='ticket',
            auth_plugin='mysql_native_password'  # Specify the authentication plugin separately
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

