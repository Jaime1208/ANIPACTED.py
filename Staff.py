class Staff():
    count_id = 0

    def __init__(self, name,gender, phone_number, email,departments, job_name, address, password, confirm_password, status, datecreated):
        Staff.count_id += 1
        self.__staff_id = Staff.count_id
        self.__name = name
        self.__gender = gender
        self.__phone_number = phone_number
        self.__email = email
        self.__departments = departments
        self.__job_name = job_name
        self.__address = address
        self.__password = password
        self.__confirm_password = confirm_password
        self.__status = status
        self.__datecreated = datecreated

    # accessor methods
    def get_staff_id(self):
        return self.__staff_id

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_phone_number(self):
        return self.__phone_number

    def get_email(self):
        return self.__email

    def get_departments(self):
        return self.__departments

    def get_job_name(self):
        return self.__job_name

    def get_address(self):
        return self.__address

    def get_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password

    def get_status(self):
        return self.__status

    def get_datecreated(self):
        return self.__datecreated

    # mutator methods
    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    def set_name(self, name):
        self.__name = name

    def set_gender(self,gender):
        self.__gender = gender

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_email(self, email):
        self.__email = email

    def set_departments(self, departments):
        self.__departments = departments

    def set_job_name(self, job_name):
        self.__job_name = job_name

    def set_address(self, address):
        self.__address = address

    def set_password(self,password):
        self.__password = password

    def set_confirm_password(self,confirm_password):
        self.__confirm_password = confirm_password

    def set_status(self,status):
        self.__status = status

    def set_datecreated(self,datecreated):
        self.__datecreated = datecreated
