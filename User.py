class User:
    def __init__(self, user_id, username, password, role_id, role_name):
        self._user_id = user_id
        self._username = username
        self._password = password
        self._role_id = role_id
        self._role_name = role_name

    def as_dict(self):
        return {
            'UserID': self._user_id,
            'Username': self._username,
            'Password': self._password,
            'RoleID': self._role_id,
            'RoleName': self._role_name
        }

    # Getters
    def get_user_id(self):
        return self._user_id

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_role_id(self):
        return self._role_id

    def get_role_name(self):
        return self._role_name

    # Setters
    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def set_role_id(self, role_id):
        self._role_id = role_id
