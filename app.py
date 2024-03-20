from flask import Flask, render_template, request, redirect, url_for, session
from DBConnectUser import connect_to_database as connect_user_database, close_database_connection as close_user_database_connection
from DBConnectTicket import connect_to_database as connect_ticket_database, close_database_connection as close_ticket_database_connection
from TicketDao import *
from UserDao import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
user_dao = UserDAO(connect_user_database())
ticket_dao = TicketDao(connect_ticket_database())

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        user = user_dao.authenticate_user(username, password)
        if user:
            session['username'] = user['Username']
            user_role = user['RoleName']  # Obtain role directly from user object
            if user_role == 'admin':
                return redirect(url_for('show_tickets'))
            else:
                return redirect(url_for('show_tickets'))
        else:
            return "Invalid username or password"
    return render_template('login.html')


@app.route('/tickets.html')
def show_tickets():
    # Connect to the database
    conn = connect_to_database()
    if conn:
        # Call the get_tickets function to fetch all tickets from the database
        tickets = ticket_dao.get_tickets()
        # Close the database connection
        close_database_connection(conn)

        # Check if tickets is None
        if tickets is None:
            return "No tickets found"  # Return an appropriate message

        # Pass the tickets data to the template for rendering
        return render_template('tickets.html',
                               tickets=tickets, headers=['Ticket #',
                                                         'Content', 'State', 'Created Date', 'Modified Date'])
    else:
        return "Failed to connect to the database"

@app.route('/ticketDetail.html')
def ticket_detail():
    ticket_number = request.args.get('ticket_number')
    print(ticket_number)
    try:
        ticket_details = ticket_dao.get_ticket_details(ticket_number)  # Pass 'conn' here
        print(ticket_details)
        print(ticket_number)
        if ticket_details:
            return render_template('ticketDetail.html', ticket=ticket_details)
        else:
            return f"Ticket with number {ticket_number} not found."
    except Exception as e:
        return f"Error fetching ticket details: {str(e)}"

if __name__ == '__main__':
    app.run()
