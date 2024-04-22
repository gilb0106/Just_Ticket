import mysql.connector
import datetime

class UserActivityDAO:
    def __init__(self, conn):
        self.conn = conn

    def log_activity(self, user_id, activity_type):
        try:
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO useractivity (UserID, ActivityType, ActivityDate) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (user_id, activity_type, datetime.datetime.now()))
            self.conn.commit()
            cursor.close()
            print("User activity logged successfully")
        except mysql.connector.Error as err:
            print(f"Error logging user activity: {err}")

    def get_user_activity(self, user_id=None, activity_type=None, start_date=None, end_date=None):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM useractivity WHERE 1=1"
            params = []

            if user_id is not None:
                query += " AND UserID = %s"
                params.append(user_id)
            if activity_type is not None:
                query += " AND ActivityType = %s"
                params.append(activity_type)
            if start_date is not None:
                query += " AND ActivityDate >= %s"
                params.append(start_date)
            if end_date is not None:
                query += " AND ActivityDate <= %s"
                params.append(end_date)

            cursor.execute(query, params)
            activities = cursor.fetchall()
            cursor.close()
            return activities
        except mysql.connector.Error as err:
            print(f"Error fetching user activity: {err}")
            return None