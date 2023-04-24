# Event class
class Event:
    count_id = 0

    # initializer method
    def __init__(self, title_name, event_date, tagscategory, event_desc, status, datecreated):
        Event.count_id += 1
        self.count_id = Event.count_id
        self.__title_name = title_name
        self.__event_date = event_date
        self.__tagscategory = tagscategory
        self.__event_desc = event_desc
        self.__status = status
        self.__datecreated = datecreated

    # accessor methods
    def get_event_id(self):
        return self.count_id

    def get_title_name(self):
        return self.__title_name

    def get_event_date(self):
        return self.__event_date

    def get_tagscategory(self):
        return self.__tagscategory

    def get_event_desc(self):
        return self.__event_desc

    def get_status(self):
        return self.__status

    def get_datecreated(self):
        return self.__datecreated




    # mutator methods

    def set_title_name(self, title_name):
        self.__title_name = title_name

    def set_event_date(self, event_date):
        self.__event_date = event_date

    def set_tagscategory(self, tagscategory):
        self.__tagscategory = tagscategory

    def set_event_desc(self, event_desc):
        self.__event_desc = event_desc

    def set_status(self, status):
        self.__status = status

    def set_datecreated(self, datecreated):
        self.__datecreated = datecreated


