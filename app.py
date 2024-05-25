from flask import Flask, render_template, request, redirect, url_for, session, Response, flash

from DBConnectUser import connect_to_database
from UserActivityDAO import UserActivityDAO
from UserDao import UserDAO
from TicketDao import TicketDao
from datetime import datetime

app = Flask(__name__, static_url_path='/static')  # Manually declaring static path for css, js
app.secret_key = 'sadfasdfasdfsafd' # Manual session key for now, to use with session object

# Create database connections
user_conn = connect_to_database()
ticket_conn = connect_to_database()

# Instantiate DAOs with database connections
user_dao = UserDAO(user_conn)
ticket_dao = TicketDao(ticket_conn)
user_activity = UserActivityDAO(user_conn)


@app.route('/')  # First page that loads when you go to host, homepage index.html
def home():
    return render_template('index.html')


@app.route('/logout')  # Logout functionality, cancels session
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/register.html')  # Register page that will be in the works
def register():
    return render_template('register.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        user = user_dao.authenticate_user(username, password)
        user_id = user_dao.get_user_id(username)
        if user:  # Adjusted to use OOP principles
            session['username'] = user.get_username()
            session['UserID'] = user.get_user_id()
            session['RoleName'] = user.get_role_name()
            if user.get_role_id() == 1:
                user_activity.log_activity(user_id, 'login')
                return redirect(url_for('dashboard', dashboard_type='agent'))
            else:
                return redirect(url_for('dashboard', dashboard_type='customer'))
        else:
            error_message = "Invalid username or password"
    return render_template('login.html', error_message=error_message)


@app.route('/dashboard.html')
def dashboard():
    if 'username' in session:
        role_name = session.get('RoleName')
        user_id = session.get('UserID')

        if role_name == 'agent':
            all_tickets = ticket_dao.get_tickets()
            in_progress_tickets = [ticket for ticket in all_tickets if ticket.get_state() == 'inprogress']
            open_tickets = [ticket for ticket in all_tickets if ticket.get_state() == 'open']
            closed_tickets = [ticket for ticket in all_tickets if ticket.get_state() == 'closed']
            return render_template('dashboard.html', in_progress_tickets=in_progress_tickets, open_tickets=open_tickets,
                                   closed_tickets=closed_tickets)

        elif role_name == 'customer':
            user_tickets = ticket_dao.get_user_tickets(user_id)
            active_tickets = [ticket for ticket in user_tickets if ticket.get_state() != 'closed']
            past_tickets = [ticket for ticket in user_tickets if ticket.get_state() == 'closed']
            return render_template('dashboard.html', active_tickets=active_tickets, past_tickets=past_tickets)

        else:
            return "Invalid role"
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
        user_role = session.get('RoleName')
        modified_date = datetime.now()

        ticket_agent = None

        previous_state = ticket_dao.get_ticket_state(ticket_number)

        if user_role != 'agent' and previous_state != new_state:
            flash("You don't have permission to change the ticket state.", 'error')
            return redirect(url_for('ticket_detail', ticket_number=ticket_number))

        if new_state != previous_state:
            # Log activity for state change
            if new_state == 'inprogress':
                user_activity.log_activity(user_id, 'ticket_inprogress')  # Log user state change with enum value
            elif new_state == 'closed':
                user_activity.log_activity(user_id, 'ticket_closed')  # Log user state change with enum value

            # Update the ticket agent
            if new_state in ['inprogress', 'closed']:
                ticket_agent = user_id

        # Check if comment is empty
        if comment:
            ticket_dao.add_comment(ticket_number, comment, user_id, modified_date)
            user_activity.log_activity(user_id, 'ticket_comment')  # Log user comment with enum value

        # Update the ticket with the new content, state, and agent responsible for the ticket
        ticket_dao.update_ticket(ticket_number, content, new_state, modified_date, ticket_agent)

        return redirect(url_for('ticket_detail', ticket_number=ticket_number))


@app.route('/createticket.html')  # Render html page
def create_ticket_page():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('createticket.html', current_date=current_date)


@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if 'username' in session:
        if request.method == 'POST':
            content = request.form['content']
            created_by = session['username']
            user_id = user_dao.get_user_id(created_by)
            created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if ticket_dao.create_ticket(content, created_by, created_date):
                user_activity.log_activity(user_id, 'ticket_create')
                flash("Ticket created successfully", 'success')  # Flash success message
                return redirect(url_for('dashboard', dashboard_type='customer'))
            else:
                return "Failed to create ticket"
        elif request.method == 'GET':
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return render_template('createticket.html', current_date=current_date)
    else:
        return redirect(url_for('login'))

@app.route('/query_ticket.html', methods=['GET'])
def query_ticket():
    if 'username' in session:  # Ensure user is logged in
        role_id = session.get('RoleID')
        role_name = session.get('RoleName')

        if request.method == 'POST':
            # Extract form data
            state = request.form.get('state')
            created_date = request.form.get('created_date')
            modified_date = request.form.get('modified_date')

            # Query tickets based on the provided filters
            filtered_tickets = ticket_dao.query_tickets(state, created_date, modified_date)

            if filtered_tickets:
                # Render the ticket data as HTML
                return render_template('ticket_data.html', tickets=filtered_tickets, role_id=role_id,
                                       role_name=role_name)
            else:
                return "No tickets found matching the criteria."
        else:
            return render_template('query_ticket.html', role_id=role_id, role_name=role_name)
    else:
        return redirect(url_for('login')) # If no user session redirect to login


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
            ticket_data_html = render_template('ticket_data.html', tickets=filtered_tickets)
            return render_template('query_ticket.html', ticket_data_html=ticket_data_html)
        else:
            return render_template('query_ticket.html', message="No tickets found matching the criteria.")
    else:
        return redirect(url_for('login')) # If no user session redirect to login


@app.route('/export_csv', methods=['POST'])
def export_csv():
    if 'username' in session:  # Ensure user is logged in
        # Extract ticket data from the request form
        tickets = request.form.getlist('tickets[]')

        if tickets:
            # Create CSV content
            csv_content = "Ticket Number,Content,State,Created Date,Modified Date,Agent Username\n"
            for ticket in tickets:
                csv_content += ticket + "\n"

            # Return CSV file as response
            return Response(
                csv_content,
                mimetype="text/csv",
                headers={"Content-disposition": "attachment; filename=tickets.csv"}
            )
        else:
            return "No tickets selected for export."
    else:
        return redirect(url_for('login')) # If no user session redirect to login


if __name__ == '__main__':
    app.run()
