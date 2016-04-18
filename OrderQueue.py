#Order Station, this takes a while because you can't understand a god damn thing the person taking the order is saying
import rvgs.py

class OrderQueue:
    queueSize = 0
    can_move = True
    maximum = 0

    def get_service(self):
        total_time = 0
        num_items = rvgs.uniform(1,6)
        for i in range(0, num_items):
            total_time = total_time + rvgs.geometric(.02)

    def add_to_queue(self): #arrival
        self.queueSize += 1

    def get_queue_size(self):
        return self.queueSize

    def set_max(self, max):
        self.maximum = max

    def order_complete(self):
        self.queueSize -= 1