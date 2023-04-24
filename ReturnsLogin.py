class Login:

    def __init__(self, name, password):
        self.__name = name
        self.__password = password
    # accessor methods

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password

    # mutator methods

    def set_name(self, name):
        self.__name = name

    def set_password(self, password):
        self.__password = password

