__author__ = 'Derek'

from enum import Enum

class eventType(Enum):
    arrival = 1
    orderCompletion = 2
    paymentCompletion = 3
    pickupCompletion = 4

class Event:
    eventType = -1 # this is for error checking. they are technicaly PUBLIC so we will change them in the program by using event.eventType(1) etc
    time = -1 # same as above comment
    def __lt__(self, other): #overrides the built in comparison method so we can specify the values to compare
        return self.time < other.time
