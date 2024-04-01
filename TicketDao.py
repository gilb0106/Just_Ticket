import mysql
from DBConnectTicket import connect_to_database, close_database_connection

class TicketDao:
    def __init__(self, conn):
        self.conn = conn

    def get_tickets(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Ticket")
            result = cursor.fetchall()
            for row in result:
                print(row)
            return result
        except mysql.connector.Error as err:
            print(f"Error executing SQL query: {err}")
        finally:
            cursor.close()

    def get_ticket_details(self, ticket_number):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Ticket WHERE TicketNumber = %s", (ticket_number,))
            ticket_details = cursor.fetchone()
            cursor.close()
            return ticket_details
        except mysql.connector.Error as err:
            print(f"Error fetching ticket details: {err}")
            return None
    def update_ticket(self, ticket_number, content, state):
        try:
            cursor = self.conn.cursor()
            update_query = "UPDATE Ticket SET TicketContent = %s, State = %s WHERE TicketNumber = %s"
            cursor.execute(update_query, (content, state, ticket_number))
            self.conn.commit()
            cursor.close()
            print("Ticket updated successfully")
        except mysql.connector.Error as err:
            print(f"Error updating ticket: {err}")

    def add_comment_to_ticket(self, ticket_number, comment):
        try:
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO TicketComment (TicketNumber, CommentContent) VALUES (%s, %s)"
            cursor.execute(insert_query, (ticket_number, comment))
            self.conn.commit()
            cursor.close()
            print("Comment added to ticket successfully")
        except mysql.connector.Error as err:
            print(f"Error adding comment to ticket: {err}")


    def get_ticket_details(self, ticket_number):
        try:
            if not hasattr(self.conn, 'cursor'):
                raise AttributeError("The provided connection object does not have a cursor attribute.")
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT t.*, u.Username FROM Ticket t JOIN User u ON t.UserID = u.UserID WHERE t.TicketNumber = %s", (ticket_number,))
            ticket_details = cursor.fetchone()
            cursor.close()
            return ticket_details
        except AttributeError as e:
            print(f"Attribute error: {e}")
        except mysql.connector.Error as err:
            print(f"Error fetching ticket details: {err}")
        return None

    def get_ticket_comments(self, ticket_number):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM TicketComment WHERE TicketNumber = %s", (ticket_number,))
            comments = cursor.fetchall()
            cursor.close()
            return comments
        except mysql.connector.Error as err:
            print(f"Error fetching ticket comments: {err}")
            return None
    def get_user_tickets(self, user_id):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Ticket WHERE UserID = %s", (user_id,))
            user_tickets = cursor.fetchall()
            cursor.close()
            return user_tickets
        except mysql.connector.Error as err:
            print(f"Error fetching user tickets: {err}")
            return None

    def get_newest_unused_ticket_number(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(TicketNumber) FROM Ticket")
            newest_ticket_number = cursor.fetchone()[0]
            cursor.close()
            return newest_ticket_number
        except mysql.connector.Error as err:
            print(f"Error fetching newest unused ticket number: {err}")
            return None

    def create_ticket(self, ticket_number, content, created_by, created_date):
        try:
            # Import user_dao locally within the function
            from app import user_dao
            cursor = self.conn.cursor()
            user_id = user_dao.get_user_id(created_by)
            insert_query = "INSERT INTO Ticket (TicketNumber, TicketContent, UserID, Created) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (ticket_number, content, user_id, created_date))
            self.conn.commit()
            cursor.close()
            print("Ticket created successfully")
        except mysql.connector.Error as err:
            print(f"Error creating ticket: {err}")


