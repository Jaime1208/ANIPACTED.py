

class Return:
    count_id = 0

    def __init__(self, name, orderid, returnreason, contact, address, returnoption, returndate, remarks, status):
        Return.count_id += 1
        self.__name = name
        self.__orderid = orderid
        self.__returnreason = returnreason
        self.__contact = contact
        self.__remarks = remarks
        self.__return_id = Return.count_id
        self.__returnoption = returnoption
        self.__returndate = returndate
        self.__address = address
        self.__status = status

    # accessor methods
    def get_return_id(self):
        return self.__return_id

    def get_name(self):
        return self.__name

    def get_orderid(self):
        return self.__orderid

    def get_returnreason(self):
        return self.__returnreason

    def get_contact(self):
        return self.__contact

    def get_address(self):
        return self.__address

    def get_returnoption(self):
        return self.__returnoption

    def get_returndate(self):
        return self.__returndate

    def get_remarks(self):
        return self.__remarks

    def get_status(self):
        return self.__status

    # mutator methods
    def set_return_id(self, return_id):
        self.__return_id = return_id

    def set_name(self, name):
        self.__name = name

    def set_orderid(self, orderid):
        self.__orderid = orderid

    def set_returnreason(self, returnreason):
        self.__returnreason = returnreason

    def set_contact(self, contact):
        self.__contact = contact

    def set_address(self, address):
        self.__address = address

    def set_returnoption(self, returnoption):
        self.__returnoption = returnoption

    def set_returndate(self, returndate):
        self.__returndate = returndate

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_status(self, status):
        self.__status = status


