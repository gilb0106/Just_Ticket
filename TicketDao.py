import mysql
from DBConnectTicket import connect_to_database, close_database_connection

class TicketDao:
    def __init__(self, conn):
        self.conn = conn
    def get_tickets(self):
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM ticket")
                result = cursor.fetchall()
                for row in result:
                    print(row)
                return result
            except mysql.connector.Error as err:
                print(f"Error executing SQL query: {err}")
            finally:
                cursor.close()
                close_database_connection(connection)
    def get_ticket_details(self, ticket_number):
        try:
            if not hasattr(self.conn, 'cursor'):
                raise AttributeError("The provided connection object does not have a cursor attribute.")
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM ticket WHERE TicketNumber = %s", (ticket_number,))
            ticket_details = cursor.fetchone()
            cursor.close()
            return ticket_details
        except AttributeError as e:
            print(f"Attribute error: {e}")
        except mysql.connector.Error as err:
            print(f"Error fetching ticket details: {err}")
        return None