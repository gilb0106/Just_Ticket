from flask import Flask, render_template, request, redirect, url_for, session
from DBConnectUser import connect_to_database as connect_user_database, close_database_connection as close_user_database_connection
from DBConnectTicket import connect_to_database as connect_ticket_database, close_database_connection as close_ticket_database_connection
from TicketDao import *
from UserDao import *
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
user_dao = UserDAO(connect_user_database())
ticket_dao = TicketDao(connect_ticket_database())

@app.route('/')
def home():
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
            if user['RoleID'] == 1:
                return redirect(url_for('show_tickets'))
            else:
                return redirect(url_for('show_user_tickets'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/admindashboard.html')
def show_tickets():
    if 'username' in session:
        tickets = ticket_dao.get_tickets()
        if tickets is None:
            return "No tickets found"
        return render_template('admindashboard.html',
                               tickets=tickets,
                               headers=['Ticket #', 'Content', 'State', 'Created Date', 'Modified Date'])
    else:
        return redirect(url_for('login'))

@app.route('/userdashboard.html')
def show_user_tickets():
    if 'username' in session:
        user_id = user_dao.get_user_id(session['username'])
        tickets = ticket_dao.get_user_tickets(user_id)  # Get tickets by user
        if tickets is None:
            return "No tickets found"
        return render_template('userdashboard.html',
                               tickets=tickets,
                               headers=['Ticket #', 'Content', 'State', 'Created Date', 'Modified Date'])
    else:
        return redirect(url_for('login'))

@app.route('/ticketDetail.html')
def ticket_detail():
    ticket_number = request.args.get('ticket_number')
    try:
        ticket_details = ticket_dao.get_ticket_details(ticket_number)
        if ticket_details:
            user_id = ticket_details['UserID']
            username = user_dao.get_username_by_id(user_id)
            comments = ticket_dao.get_ticket_comments(ticket_number)
            return render_template('ticketDetail.html', ticket=ticket_details, username=username, comments=comments)
        else:
            return f"Ticket with number {ticket_number} not found."
    except Exception as e:
        return f"Error fetching ticket details: {str(e)}"

@app.route('/update_ticket', methods=['POST'])
def update_ticket():
    if request.method == 'POST':
        ticket_number = request.form['ticket_number']
        content = request.form['content']
        state = request.form['state']
        comment = request.form['comment']

        ticket_dao.update_ticket(ticket_number, content, state)

        ticket_dao.add_comment_to_ticket(ticket_number, comment)

        return redirect(url_for('ticket_detail', ticket_number=ticket_number))

@app.route('/createticket.html')
def create_ticket_page():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('createticket.html', current_date=current_date)

@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    if 'username' in session:
        if request.method == 'POST':
            content = request.form['content']
            created_by = session['username']
            created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            newest_ticket_number = ticket_dao.get_newest_unused_ticket_number() + 1

            ticket_dao.create_ticket(newest_ticket_number, content, created_by, created_date)

            return redirect(url_for('show_user_tickets'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()