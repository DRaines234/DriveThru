__author__ = 'Derek and Spencer'

import OrderQueue
import PaymentWindow
import PickupWindow
import rvgs
import heapq #import for heap data structure!
import Event
import EventList

order = OrderQueue()
payment = PaymentWindow()
pickup = PickupWindow()

def get_arrival():
    get_arrival().arrival_time += rvgs.exponential(2.0) #adjusting this number will adjust our inter-arrival time
    return get_arrival().arrival_time # arrival time is one of those function variable things that I cant remember the name of

class time_structure:
    def __init__(self):
        self.arrival = -1                # next arrival time
        self.orderCompletion = -1        # next order completion time
        self.paymentCompletion = -1      # next payment completion time
        self.pickupCopmletion = -1       # next pickup completion time
        self.current = -1                # current time


def run_sim(orderQueueSize, payQueueSize, pickupQueueSize, iterations):
    order.set_max = orderQueueSize
    payment.set_max = payQueueSize
    pickup.set_max = pickupQueueSize
    STOP = iterations
    infinity = STOP * 100 # should be a good bet that our simulation won't run this long
    eventList = heapq # initialize an event list as aa heapq

    get_arrival().arrival_time = 0 # initialize arrival time to 0


    t = time_structure()
    t.current = 0 # set the simulation clock to 0
    t.arrival = get_arrival() # get our first arrival time


    # set completions to infinity to show we don't have any completions yet.
    t.orderCompletion = infinity
    t.paymentCompletion = infinity
    t.pickupCopmletion = infinity

    #currently without any intake from data

    while(t.arrival < STOP): # keep running the simulation until we reach our stop time
        #check if queue is empty, then add to the queue for order window
        if order.get_queue_size < order.get_max():
            order.add_to_queue()

        #check if queue is empty, then add to the queue for payment window
        if payment.get_queue_size < payment.get_max():
            payment.add_to_queue()

        #check if queue is empty, then add to the queue for pickup window
        if pickup.get_queue_size < pickup.get_max():
            pickup.add_to_queue()

def main():
    run_sim(5,5,5,100) #q1, q2, q3, stop

if __name__ == "__main__":
    main()