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
        self.arrival = -1                # next arrival time, we keep this here just so we have a running arrival
        self.current = -1                # we have to keep track of the current time

def run_sim(orderQueueSize, payQueueSize, pickupQueueSize, iterations):
    order.set_max = orderQueueSize
    payment.set_max = payQueueSize
    pickup.set_max = pickupQueueSize
    STOP = iterations
    infinity = STOP * 100 # should be a good bet that our simulation won't run this long
    EL = EventList.EventList() # create a new event list object

    get_arrival().arrival_time = 0 # initialize arrival time to 0


    t = time_structure()
    t.current = 0 # set the simulation clock to 0

    arrival = Event.Event() # create a new event object
    t.arrival = get_arrival() # get our first arrival time, we might get rid of this
    arrival.time = t.arrival # set the objects time to t.arrival
    arrival.eventType = Event.eventType(1) # set the enum to make the event type be an arrival
    EL.scheduleEvent(arrival) # add the arrival to the event list.

    # We do not need to set the completions to infinity because it is the same as the objects not existing.


    #currently without any intake from data

    while(t.arrival < STOP): # keep running the simulation until we reach our stop time
        nextTime = EL.getNextEvent().time # BAM! get our event from the heap in the event list! and get its time element

        #------------------------------------------------------------------------------------------------
        # majority of logic goes in here

        #check if queue is empty, then add to the queue for order window
        if order.get_queue_size < order.get_max():
            order.add_to_queue() # Process an arrival in here

        #check if queue is empty, then add to the queue for payment window
        if payment.get_queue_size < payment.get_max():
            payment.add_to_queue()

        #check if queue is empty, then add to the queue for pickup window
        if pickup.get_queue_size < pickup.get_max():
            pickup.add_to_queue()


        #--------------------------------------------------------------------------------------------------
def main():
    run_sim(5,5,5,100) #q1, q2, q3, stop

if __name__ == "__main__":
    main()