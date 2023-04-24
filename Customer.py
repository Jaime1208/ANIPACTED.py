class Customer():
    count_id = 0

    def __init__(self, name, gender, birthday,occupation,phone_number,email, address,password,confirm_password,status,datecreated):
        Customer.count_id += 1
        self.__customer_id = Customer.count_id
        self.__name = name
        self.__gender = gender
        self.__birthday = birthday
        self.__occupation = occupation
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address
        self.__password = password
        self.__confirm_password = confirm_password
        self.__datecreated = datecreated
        self.__status = status


    # accessor methods
    def get_customer_id(self):
        return self.__customer_id

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_birthday(self):
        return self.__birthday

    def get_occupation(self):
        return self.__occupation

    def get_phone_number(self):
        return self.__phone_number

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password

    def get_datecreated(self):
        return self.__datecreated

    def get_status(self):
        return self.__status


    # mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_name(self, name):
        self.__name = name

    def set_gender(self,gender):
        self.__gender = gender

    def set_birthday(self, birthday):
        self.__birthday = birthday

    def set_occupation(self, occupation):
        self.__occupation = occupation

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_password(self,password):
        self.__password = password

    def set_confirm_password(self,confirm_password):
        self.__confirm_password = confirm_password

    def set_datecreated(self,datecreated):
        self.__datecreated = datecreated

    def set_status(self,status):
        self.__status = status
