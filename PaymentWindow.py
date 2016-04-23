#Payment window, aka shit where's my wallet.
import rvgs
class PaymentWindow:

    can_move = True
    queueSize = 0
    maximum = 0
    largestAmt = 0

    def get_service(self):
        return rvgs.uniform(0,2) # given if the worker is new, types of change, register not working, uniform seems fine, and generate between 0 and three minutes, usually above .1 seems to be the lowest

    def add_to_queue(self): #arrival
        self.queueSize += 1
        if self.queueSize > self.largestAmt:
            self.largestAmt = self.queueSize

    def get_queue_size(self):
        return self.queueSize

    def set_max(self, max):
        self.maximum = max

    def get_max(self):
        return self.maximum

    def pay_complete(self):
        self.queueSize -= 1

    def getLargestSize(self):
        return self.largestAmt