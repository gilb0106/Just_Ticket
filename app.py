from flask import Flask, render_template, request

from DBConnect import connect_to_database,  close_database_connection
from Dao import  get_tickets,get_ticket_details

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

# Route for the login page
@app.route('/login.html')
def login():
    return render_template('login.html')

# Route for the registration page
@app.route('/register.html')
def register():
    return render_template('register.html')

# Python code
@app.route('/tickets.html')
def show_tickets():
    # Connect to the database
    conn = connect_to_database()
    if conn:
        # Call the get_tickets function to fetch all tickets from the database
        tickets = get_tickets(conn)
        # Close the database connection
        close_database_connection(conn)
        # Pass the tickets data to the template for rendering
        return render_template('tickets.html',
                               tickets=tickets, headers=['Ticket #',
                                                         'Content', 'State', 'Created Date', 'Modified Date'])
    else:
        return "Failed to connect to the database"

@app.route('/ticketdetail')
def show_ticket():
    # Extract ticket number from the query parameters
    ticket_number = request.args.get('ticketnumber')

    if ticket_number is None:
        return "Ticket number is missing in the request."

    # Connect to the database
    conn = connect_to_database()
    if conn:
        try:
            # Fetch the ticket details from the database
            ticket_details = get_ticket_details(conn, ticket_number)
            if ticket_details:
                # Close the database connection
                close_database_connection(conn)
                # Pass the ticket details to the template for rendering
                return render_template('ticket_detail.html', ticket=ticket_details)
            else:
                return f"Ticket with number {ticket_number} not found."
        except Exception as e:
            return f"Error fetching ticket details: {str(e)}"
    else:
        return "Failed to connect to the database."

@app.route('/ticketDetail.html')
def ticket_detail():
    ticket_number = request.args.get('ticket_number')
    # Connect to the database
    conn = connect_to_database()
    if conn:
        try:
            # Fetch the ticket details from the database based on the provided ticket number
            ticket_details = get_ticket_details(conn, ticket_number)
            if ticket_details:
                # Close the database connection
                close_database_connection(conn)
                # Pass the ticket details to the template for rendering
                return render_template('ticketDetail.html', ticket=ticket_details)
            else:
                return f"Ticket with number {ticket_number} not found."
        except Exception as e:
            return f"Error fetching ticket details: {str(e)}"
    else:
        return "Failed to connect to the database."

if __name__ == '__main__':
    app.run()
