import mysql.connector
import csv

from Ticket import Ticket


class TicketDao:
    def __init__(self, conn):
        self.conn = conn

    def get_tickets(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    ticket.TicketNumber, 
                    ticket.TicketContent, 
                    ticket.State, 
                    ticket.Created, 
                    ticket.Modified, 
                    user.Username as TicketFor
                FROM ticket
                INNER JOIN user ON ticket.UserID = user.UserID
                ORDER BY ticket.TicketNumber ASC
            """)
            result = cursor.fetchall()
            tickets = []
            for row in result:
                ticket = Ticket(
                    row['TicketNumber'],
                    row['TicketContent'],
                    row['State'],
                    row['Created'],
                    row['Modified'],
                    row['TicketFor']
                )
                tickets.append(ticket)  # Convert Ticket object to dictionary
            return tickets
        except mysql.connector.Error as err:
            print(f"Error executing SQL query: {err}")
            return None
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
    def get_ticket_state(self, ticket_number):
        try:
            cursor = self.conn.cursor()
            query = "SELECT State FROM ticket WHERE TicketNumber = %s"
            cursor.execute(query, (ticket_number,))
            state = cursor.fetchone()
            cursor.close()
            return state[0] if state else None
        except mysql.connector.Error as err:
            print(f"Error fetching ticket state: {err}")
            return None
    def update_ticket(self, ticket_number, content, state, ticket_agent=None):
        try:
            cursor = self.conn.cursor()
            update_query = "UPDATE ticket SET TicketContent = %s, State = %s, TicketAgent = %s WHERE TicketNumber = %s"
            cursor.execute(update_query, (content, state, ticket_agent, ticket_number))
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
            cursor.execute("""
                SELECT 
                    ticket.TicketNumber, 
                    ticket.TicketContent, 
                    ticket.State, 
                    ticket.Created, 
                    ticket.Modified, 
                    user.Username as TicketFor
                FROM ticket
                INNER JOIN user ON ticket.UserID = user.UserID
                WHERE ticket.UserID = %s ORDER BY ticket.TicketNumber ASC
            """, (user_id,))
            result = cursor.fetchall()
            tickets = []  # Create a list to store tickets
            for row in result:
                ticket = Ticket(
                    row['TicketNumber'],
                    row['TicketContent'],
                    row['State'],
                    row['Created'],
                    row['Modified'],
                    row['TicketFor']
                )
                tickets.append(ticket)  # Append each ticket to the list

            return tickets  # Return the list of tickets
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

    def query_tickets(self, state=None, created_date=None, modified_date=None):
        # Establish a cursor to execute SQL queries
        cursor = self.conn.cursor(dictionary=True)

        # Base SQL query to select tickets with necessary joins
        query = """
            SELECT 
                t.TicketNumber, 
                t.TicketContent AS Content, 
                t.State, 
                t.Created AS CreatedDate, 
                t.Modified AS ModifiedDate, 
                u.Username as TicketFor
            FROM 
                ticket AS t
            LEFT JOIN 
                user AS u ON t.UserID = u.UserID
        """
        # Initialize the WHERE clause
        where_clause = []
        # Add conditions to the WHERE clause based on input parameters
        if state:
            where_clause.append(f"t.State = '{state}'")
        if created_date:
            where_clause.append(f"DATE(t.Created) = '{created_date}'")
        if modified_date:
            where_clause.append(f"DATE(t.Modified) = '{modified_date}'")
        # Construct the final SQL query
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)
        # Execute the SQL query
        cursor.execute(query)
        # Fetch all the selected rows
        rows = cursor.fetchall()
        # Close the cursor
        cursor.close()

        # Create instances of Ticket class
        tickets = []
        for row in rows:
            ticket = Ticket(
                row['TicketNumber'],
                row['Content'],
                row['State'],
                row['CreatedDate'],
                row['ModifiedDate'],
                row['TicketFor']
            )
            tickets.append(ticket)

        # Return the queried tickets
        return tickets

