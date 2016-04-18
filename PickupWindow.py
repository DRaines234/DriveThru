##PickupWindow where they give you a burger with pickles when you asked for no pickles

import rvgs.py

class PickupWindow:
    can_move = True
    queueSize = 0
    maximum = 0

    def get_service(self):
        return rvgs.exponential(2) #chose exponential because it is skewed toward smaller numbers but if they mess up we have a possiblilty of getting higher numbers

    def add_to_queue(self): # arrival
        self.queueSize += 1

    def get_queue_size(self):
        return self.queueSize

    def set_max(self, max):
        self.maximum = max

    def pickup_complete(self):
        self.queueSize -= 1