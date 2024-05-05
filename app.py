from flask import Flask, render_template, request, redirect, url_for, session

from DBConnectUser import connect_to_database
from UserActivityDAO import UserActivityDAO
from UserDao import UserDAO
from TicketDao import TicketDao
import datetime

app = Flask(__name__, static_url_path='/static')
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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

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
                user_activity.log_activity(user_id, 'login')
                return redirect(url_for('dashboard', dashboard_type='agent'))
            else:
                return redirect(url_for('dashboard', dashboard_type='customer'))
        else:
            return "Invalid username or password"
    return render_template('login.html')


@app.route('/dashboard.html')
def dashboard():
    if 'username' in session:
        dashboard_type = request.args.get('dashboard_type')
        user_id = user_dao.get_user_id(session['username'])
        if dashboard_type == 'agent':
            tickets = ticket_dao.get_tickets()
            headers = ['Ticket Number', 'Content', 'State', 'Age','Created Date',  'Modified Date', 'Ticket For']
        elif dashboard_type == 'customer':
            tickets = ticket_dao.get_user_tickets(user_id)
            headers = ['Ticket #', 'Content', 'State', 'Age','Created Date', 'Modified Date']
        else:
            return "Invalid dashboard type"

        if not tickets:
            return "No tickets found"

        return render_template('dashboard.html', tickets=tickets, headers=headers)
    else:
        return redirect(url_for('login'))

@app.route('/ticketDetail.html')
def ticket_detail():
    ticket_number = request.args.get('ticket_number')
    try:
        ticket_details = ticket_dao.get_ticket_details(ticket_number)
        if ticket_details:
            user_id = ticket_details['UserID']
            user_info = user_dao.get_user_info(user_id)
            if user_info:
                username = user_info['Username']
                role_name = user_dao.get_user_role(session['username'])
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
        new_state = request.form['state']
        comment = request.form['comment']
        username = session.get('username')
        user_id = user_dao.get_user_id(username)
        user_role = user_dao.get_user_role(username)

        ticket_agent = None

        previous_state = ticket_dao.get_ticket_state(ticket_number)

        if user_role != 'agent' and previous_state != new_state:
            return "You don't have permission to change the ticket state."


        if new_state != previous_state:
            # Log activity for state change
            if new_state == 'inprogress':
                user_activity.log_activity(user_id, 'ticket_inprogress')
            elif new_state == 'closed':
                user_activity.log_activity(user_id, 'ticket_closed')

            # Update the ticket agent
            if new_state in ['inprogress', 'closed']:
                ticket_agent = user_id
        else:  # State remains the same
            # Check if comment is empty
            if comment:
                ticket_dao.add_comment(ticket_number, comment, user_id)
                # Log activity only if a comment is added
                user_activity.log_activity(user_id, 'ticket_comment')
            return redirect(url_for('ticket_detail', ticket_number=ticket_number))

        # Check if comment is empty
        if comment:
            ticket_dao.add_comment(ticket_number, comment, user_id)
            # Log activity only if a comment is added
            user_activity.log_activity(user_id, 'ticket_comment')

        # Update the ticket with the new content, state, and agent
        ticket_dao.update_ticket(ticket_number, content, new_state, ticket_agent)

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


@app.route('/query_ticket.html', methods=['GET', 'POST'])
def query_ticket():
    if 'username' in session:  # Ensure user is logged in
        if request.method == 'POST':
            # Extract form data
            state = request.form.get('state')
            created_date = request.form.get('created_date')
            modified_date = request.form.get('modified_date')

            # Query tickets based on the provided filters
            filtered_tickets = ticket_dao.query_tickets(state, created_date, modified_date)

            if filtered_tickets:
                # Render the ticket data as HTML
                return render_template('ticket_data.html', tickets=filtered_tickets)
            else:
                return "No tickets found matching the criteria."
        else:
            return render_template('query_ticket.html')
    else:
        return redirect(url_for('login'))

@app.route('/query_tickets', methods=['POST'])
def query_tickets():
    if 'username' in session:  # Ensure user is logged in
        # Extract form data
        state = request.form.get('state')
        created_date = request.form.get('created_date')
        modified_date = request.form.get('modified_date')

        # Query tickets based on the provided filters
        filtered_tickets = ticket_dao.query_tickets(state, created_date, modified_date)

        if filtered_tickets:
            # Render the ticket data as HTML
            return render_template('ticket_data.html', tickets=filtered_tickets)
        else:
            return "No tickets found matching the criteria."
    else:
        return redirect(url_for('login'))@app.route('/query_tickets', methods=['POST'])


if __name__ == '__main__':
    app.run()