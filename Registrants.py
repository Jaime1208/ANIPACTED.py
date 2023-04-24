# Registrant class
class Registrant:
    count_id = 0

    # initializer method
    def __init__(self, name, phoneno, email, gender, status, datejoined):
        Registrant.count_id += 1
        self.count_id = Registrant.count_id
        self.__name = name
        self.__phoneno = phoneno
        self.__email = email
        self.__gender = gender
        self.__status = status
        self.__datejoined = datejoined

    # accessor methods
    def get_count_id(self):
        return self.count_id

    def get_name(self):
        return self.__name

    def get_phoneno(self):
        return self.__phoneno

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_status(self):
        return self.__status

    def get_datejoined(self):
        return self.__datejoined


    # mutator methods
    def set_count_id(self,count_id):
        self.count_id = count_id

    def set_name(self, name):
        self.__name = name

    def set_phoneno(self, phoneno):
        self.__phoneno = phoneno

    def set_email(self, email):
        self.__email = email

    def set_gender(self, gender):
        self.__gender = gender

    def set_status(self, status):
        self.__status = status

    def set_datejoined(self, datejoined):
        self.__datejoined = datejoined
