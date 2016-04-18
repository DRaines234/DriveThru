#Payment window, aka shit where's my wallet.
import rvgs.py
class PaymentWindow:

    can_move = True
    queueSize = 0
    maximum = 0

    def get_service(self):
        return rvgs.uniform(0,1)

    def add_to_queue(self): #arrival
        self.queueSize += 1

    def get_queue_size(self):
        return self.queueSize

    def set_max(self, max):
        self.maximum = max