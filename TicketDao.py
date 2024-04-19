import mysql.connector

class TicketDao:
    def __init__(self, conn):
        self.conn = conn

    def get_tickets(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM ticket")
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
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT t.*, u.Username, r.RoleName FROM ticket t JOIN user u ON t.UserID = u.UserID "
                "JOIN userrole r ON u.RoleID = r.RoleID WHERE t.TicketNumber = %s",
                (ticket_number,))
            ticket_details = cursor.fetchone()
            cursor.close()
            return ticket_details
        except mysql.connector.Error as err:
            print(f"Error fetching ticket details: {err}")
            return None

    def update_ticket(self, ticket_number, content, state):
        try:
            cursor = self.conn.cursor()
            update_query = "UPDATE ticket SET TicketContent = %s, State = %s WHERE TicketNumber = %s"
            cursor.execute(update_query, (content, state, ticket_number))
            self.conn.commit()
            cursor.close()
            print("Ticket updated successfully")
        except mysql.connector.Error as err:
            print(f"Error updating ticket: {err}")

    def add_comment(self, ticket_number, comment, user_id):
        try:
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO ticketcomment (TicketNumber, CommentContent, UserID) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (ticket_number, comment, user_id))
            self.conn.commit()
            cursor.close()
            print("Comment added to ticket successfully")
        except mysql.connector.Error as err:
            print(f"Error adding comment to ticket: {err}")

    def get_ticket_comments(self, ticket_number):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
            SELECT c.*, u.Username, r.RoleName
            FROM ticketcomment c
            JOIN user u ON c.UserID = u.UserID
            JOIN userrole r ON u.RoleID = r.RoleID
            WHERE c.TicketNumber = %s
            """
            cursor.execute(query, (ticket_number,))
            comments = cursor.fetchall()
            cursor.close()
            return comments
        except mysql.connector.Error as err:
            print(f"Error fetching ticket comments: {err}")
            return None

    def get_user_tickets(self, user_id):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ticket WHERE UserID = %s", (user_id,))
            user_tickets = cursor.fetchall()
            cursor.close()
            return user_tickets
        except mysql.connector.Error as err:
            print(f"Error fetching user tickets: {err}")
            return None

    def create_ticket(self, content, created_by, created_date):
        try:
            from app import user_dao
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(TicketNumber) FROM ticket")
            newest_ticket_number = cursor.fetchone()[0] or 0
            cursor.close()
            user_id = user_dao.get_user_id(created_by)
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO ticket (TicketNumber, TicketContent, UserID, Created) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (newest_ticket_number + 1, content, user_id, created_date))
            self.conn.commit()
            cursor.close()
            print("Ticket created successfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error creating ticket: {err}")
            return False
