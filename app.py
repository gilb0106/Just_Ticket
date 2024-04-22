from flask import Flask, render_template, request, redirect, url_for, session

from DBConnectUser import connect_to_database
from UserActivityDAO import UserActivityDAO
from UserDao import UserDAO
from TicketDao import TicketDao
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Create database connections
user_conn = connect_to_database()
ticket_conn = connect_to_database()

# Instantiate DAOs with database connections
user_dao = UserDAO(user_conn)
ticket_dao = TicketDao(ticket_conn)
user_activity = UserActivityDAO(user_conn)


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
        user_id = user_dao.get_user_id(username)
        if user:
            session['username'] = user['Username']
            if user['RoleID'] == 1:
                user_activity.log_activity(user_id,'login')
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
        if not tickets:
            return "No tickets found"
        return render_template('agentdashboard.html',
                               tickets=tickets,
                               headers=['Ticket Number', 'Content', 'State', 'Created Date', 'Modified Date', 'Ticket For'])
    else:
        return redirect(url_for('login'))
@app.route('/userdashboard.html')
def show_user_tickets():
    if 'username' in session:
        user_id = user_dao.get_user_id(session['username'])
        tickets = ticket_dao.get_user_tickets(user_id)
        if tickets is None:
            return "No tickets found"
        return render_template('customerdashboard.html',
                               tickets=tickets,
                               headers=['Ticket #', 'Content', 'State', 'Created Date', 'Modified Date'])
    else:
        return redirect(url_for('login'))

@app.route('/ticketDetail.html')
def ticket_detail():
    ticket_number = request.args.get('ticket_number')
    try:
        ticket_details = ticket_dao.get_ticket_details(ticket_number)
        print("Ticket details:", ticket_details)  # Add this line for debugging
        if ticket_details:
            user_id = ticket_details['UserID']
            user_info = user_dao.get_user_info(user_id)
            print("User info:", user_info)  # Add this line for debugging
            if user_info:
                username = user_info['Username']
                role_name = user_info
                comments = ticket_dao.get_ticket_comments(ticket_number)
                return render_template('ticketDetail.html', ticket=ticket_details, username=username,
                                       role_name=role_name, comments=comments)
            else:
                return f"User info not found for user ID: {user_id}"
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
        username = session.get('username')
        user_id = user_dao.get_user_id(username)
        print("Received state:", state)  # Print received state for debugging
        ticket_agent = None
        if state == 'inprogress':
            ticket_agent = user_id
        elif state == 'closed':
            ticket_agent = user_id

        ticket_dao.update_ticket(ticket_number, content, state, ticket_agent)
        ticket_dao.add_comment(ticket_number, comment, user_id)
        user_activity.log_activity(user_id, 'ticket_update')
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
            user_id = user_dao.get_user_id(created_by)
            created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if ticket_dao.create_ticket(content, created_by, created_date):
                user_activity.log_activity(user_id, 'ticket_create')
                return redirect(url_for('show_user_tickets'))
            else:
                return "Failed to create ticket"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
