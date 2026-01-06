# import statements
from datetime import timedelta

# text colors for UI outputs
RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'


# "Package" class to hold the data for the individual packages
class Package:

    # Constructor that takes input and assigns it to the appropriate variables within each package object
    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, weight, notes, loading_time,
                 delivery_time, delivery_status, truck, driver):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight = weight + ' KILO' if weight == '1' else weight + ' KILOS'
        self.notes = '"' + notes.strip() + '"' if notes else None
        self.loading_time = loading_time
        self.delivery_time = delivery_time
        self.delivery_status = delivery_status
        self.truck = truck
        self.driver = driver

    # "update" function to look up the delivery status of each package
    def update(self, timestamp):
        if self.package_id in (6, 9, 25, 28, 32):  # if the package has special constraints...
            self.special_cases(timestamp)  # ...run the "special_cases" function

        if self.delivery_time < timestamp:  # if the package has been delivered by the timestamp...
            self.delivery_status = 'DELIVERED'  # ...set the package's delivery status to 'DELIVERED'
        elif self.loading_time < timestamp:  # if the package has left the hub by the timestamp (but not been delivered)...
            self.delivery_status = 'IN TRANSIT'  # ...set the package's delivery status to 'IN TRANSIT'
        elif self.notes == '"Delayed on flight---will not arrive to depot until 9:05 am"':  # if the package is still delayed by the timestamp...
            self.delivery_status = 'DELAYED'  # ...set the package's delivery status to 'DELAYED'
        else:  # if the package is still at the hub by the timestamp...
            self.delivery_status = 'AT HUB'  # ...set the package's delivery status to 'AT HUB'

    # "special_cases" function to handle packages with special constraints
    def special_cases(self, timestamp):
        if self.package_id == 9:  # if the package is the one with the changing address...
            if timestamp < timedelta(hours=10, minutes=20):  # ...and the timestamp is before the address update...
                # ...set the package's address and notes to the incorrect values
                self.address = '300 State St'
                self.zipcode = '84103'
                self.notes = '"Wrong address listed"'
            else:  # ...and the timestamp is after the address update...
                # ...set the package's address and notes to the correct values
                self.address = '410 S State St'
                self.zipcode = '84111'
                self.notes = '"Address fixed"'
        else:  # if the package is one that is delayed...
            if timestamp < timedelta(hours=9, minutes=5):  # ...and the timestamp is before the package's arrival...
                self.notes = '"Delayed on flight---will not arrive to depot until 9:05 am"'  # ...set the package notes to the pre-arrival message
            else:  # ...and the timestamp is after the package's arrival...
                self.notes = '"Package arrived at depot"'  # ...set the package notes to the post-arrival message

    # "__str__" function to allow easy printing of "package" objects for the UI
    def __str__(self):
        color = None  # initialize a color variable that will change depending on the delivery status of the package

        if self.delivery_status == 'DELIVERED':  # if the package has been delivered...
            return f'{GREEN}[{str(self.package_id)}, {str(self.delivery_status)} ({self.delivery_time}), {str(self.address)}, {str(self.city)}, {str(self.zipcode)}, {str(self.delivery_deadline)}, {str(self.weight)}, {str(self.loading_time)}, {str(self.truck)}, {str(self.driver)}, {str(self.notes)}]{RESET}'  # ...print all the package data to the console in green
        elif self.delivery_status == 'IN TRANSIT':  # if the package is still in transit...
            return f'{YELLOW}[{str(self.package_id)}, {str(self.delivery_status)}, {str(self.address)}, {str(self.city)}, {str(self.zipcode)}, {str(self.delivery_deadline)}, {str(self.weight)}, {str(self.loading_time)}, {str(self.truck)}, {str(self.driver)}, {str(self.notes)}]{RESET}'  # ...return all the package data (minus the delivery time) to the console in yellow
        elif self.delivery_status == 'AT HUB':  # if the package is still at the hub...
            if self.package_id == 9 and self.address == '300 State St':  # ...and it's the package with the wrong address (pre-update)...
                color = BLUE  # ...color the package blue to distinguish it
            else:  # ...and it's a normal package...
                color = RED  # ...color the package red
        elif self.delivery_status == 'DELAYED':  # if the package is one of the delayed package (pre-arrival)...
            color = PURPLE  # ...color the package purple to distinguish it

        # for packages still at the hub (or delayed), print all the data (minus the delivery time, loading time, truck, and driver) to the console in red (or purple if delayed)
        return f'{color}[{str(self.package_id)}, {str(self.delivery_status)}, {str(self.address)}, {str(self.city)}, {str(self.zipcode)}, {str(self.delivery_deadline)}, {str(self.weight)}, {str(self.notes)}]{RESET}'

    # "__repr__" function to allow easy printing of "package" objects for easy testing and debugging (not used)
    def __repr__(self):
        return self.__str__()  # return the same value as "__str()__"
