class Ticket:
    def __init__(self, ticket_number, content, state, created_date, modified_date, user_id):
        self._ticket_number = ticket_number
        self._content = content
        self._state = state
        self._created_date = created_date
        self._modified_date = modified_date
        self._user_id = user_id

    def as_dict(self): # need to pass dictionary created cursor sql query, constructor wont work right without
        return {
            'TicketNumber': self._ticket_number,
            'TicketContent': self._content,
            'State': self._state,
            'Created': self._created_date,
            'Modified':self._modified_date,
            'TicketFor': self._user_id
        }

    # Getters
    def get_ticket_number(self):
        return self._ticket_number

    def get_content(self):
        return self._content

    def get_state(self):
        return self._state

    def get_created_date(self):
        return self._created_date

    def get_modified_date(self):
        return self._modified_date

    def get_user_id(self):
        return self._user_id

    # Setters
    def set_ticket_number(self, ticket_number):
        self._ticket_number = ticket_number

    def set_content(self, content):
        self._content = content

    def set_state(self, state):
        self._state = state

    def set_created_date(self, created_date):
        self._created_date = created_date

    def set_modified_date(self, modified_date):
        self._modified_date = modified_date
