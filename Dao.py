import mysql

from DBConnect import connect_to_database, close_database_connection


def get_tickets(conn):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM ticket")
            result = cursor.fetchall()
            for row in result:
                print(row)
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing SQL query: {err}")
        finally:
            # Close the database connection
            close_database_connection(connection)


def get_ticket_details(conn, ticket_number):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ticket WHERE TicketNumber = %s", (ticket_number,))
        ticket_details = cursor.fetchone()
        cursor.close()
        return ticket_details
    except mysql.connector.Error as err:
        print(f"Error fetching ticket details: {err}")
        return None
