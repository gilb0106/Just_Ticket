import mysql

from DBConnectUser import connect_to_database

class UserDAO:
    def __init__(self, conn):
        self.conn = conn

    def authenticate_user(self, username, password):
        try:
            query = """
            SELECT u.*, r.RoleName
            FROM User u
            JOIN UserRole r ON u.RoleID = r.RoleID
            WHERE u.Username = %s AND u.Password = %s
            """
            cursor = self.conn.cursor(dictionary=True)  # Fetch results as dictionary
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            if result:
                print(f"User authenticated: {result}")
            else:
                print("Authentication failed: User not found or invalid credentials")
            return result
        except mysql.connector.Error as e:
            print(f"Error authenticating user: {e}")
            return None
    def get_user_role(self, username):
        try:
            query = ("SELECT r.RoleName FROM User u "
                     "JOIN UserRole r ON u.RoleID = r.RoleID "
                     "WHERE u.Username = %s")
            cursor = self.conn.cursor()
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result['RoleName'] if result else None
        except Exception as e:
            print(f"Error retrieving user role: {e}")
            return None


