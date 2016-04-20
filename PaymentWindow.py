#Payment window, aka shit where's my wallet.
import rvgs
class PaymentWindow:

    can_move = True
    queueSize = 0
    maximum = 0
    largestAmt = 0

    def get_service(self):
        return rvgs.exponential(2) # for simplicity making the payment the same as the pickup, since food cooking time should be irrelevant, each window should have the same amount of service

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