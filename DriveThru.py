__author__ = 'Derek and Spencer'

import OrderQueue
import PaymentWindow
import PickupWindow
import rvgs
import heapq #import for heap data structure!
import Event
import EventList

order = OrderQueue.OrderQueue()
payment = PaymentWindow.PaymentWindow()
pickup = PickupWindow.PickupWindow()


def get_arrival():
    get_arrival.arrival_time += rvgs.exponential(2.0) #adjusting this number will adjust our inter-arrival time
    return get_arrival.arrival_time # arrival time is one of those function variable things that I cant remember the name of

class time_structure:
    def __init__(self):
        self.arrival = -1                # next arrival time, we keep this here just so we have a running arrival
        self.current = -1                # we have to keep track of the current time

def run_sim(payQueueSize, pickupQueueSize, iterations):
    totalCars = 0
    arrivalCount = 0
    orderCompleteCount = 0
    paymentCompleteCount = 0
    processCompleteCount = 0
    payment.set_max(payQueueSize)
    pickup.set_max(pickupQueueSize)
    STOP = iterations
    infinity = STOP * 100 # should be a good bet that our simulation won't run this long
    EL = EventList.EventList() # create a new event list object

    get_arrival.arrival_time = 0 # initialize arrival time to 0


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
        event = EL.getNextEvent()
        nextTime = event.time # BAM! get our event from the heap in the event list! and get its time element

        #Heres where we'd update integrals if we use them

        t.current = nextTime #updates clock
        #------------------------------------------------------------------------------------------------
        # majority of logic goes in here

        #process arrival
        if event.eventType.value == 1:
            order.add_to_queue() #add one car to the order window structure
            totalCars = totalCars + 1 #add one to total cars that have gone through drive through
            #check if next queue has room, if it does , schedule a completions because we can fit a car in
            if payment.get_queue_size() < payment.get_max():
                orderComplete = Event.Event()
                orderComplete.eventType = Event.eventType(2)#register event as an order completion
                orderComplete.time = t.current + order.get_service() #calculate service time and add it to curr time to get completion time
                EL.scheduleEvent(orderComplete) #add to event list

            arrival = Event.Event() #schedule next arrival
            t.arrival = get_arrival()
            arrival.time = t.arrival
            arrival.eventType = Event.eventType(1) #set this event as an type arrival
            EL. scheduleEvent(arrival) #add arrival to event list
            print("arrival", t.current)
            arrivalCount += 1

        #process order completion
        elif event.eventType.value == 2:
            order.order_complete() #removes a car from the order queue
            #make an order can move event here?
            payment.add_to_queue() #adds the car to the payment window
            # check if payment window has room
            if pickup.get_queue_size() < pickup.get_max():
                paymentComplete = Event.Event()
                paymentComplete.eventType = Event.eventType(3) #register it as a payment complete
                paymentComplete.time = t.current + payment.get_service()
                EL.scheduleEvent(paymentComplete) #add to event list
                print("order complete", t.current)
                orderCompleteCount += 1

        #payment completion
        elif event.eventType.value == 3:
            payment.pay_complete() #remove  from payment window
            # make a payment can move event here?
            pickup.add_to_queue() # add car to pickup queue
            pickupComplete = Event.Event()
            pickupComplete.eventType = Event.eventType(4) #register it as a pickup completion
            pickupComplete.time = t.current + pickup.get_service()
            EL.scheduleEvent(pickupComplete) # add to event list
            print("payment complete", t.current)
            paymentCompleteCount += 1

        #process pickup
        elif event.eventType.value == 4:
            pickup.pickup_complete() #remove car from pickup
            print("process complete", t.current)
            processCompleteCount += 1
    print("totalCars:", totalCars)
    print("arrivalCount:", arrivalCount)
    print("orderCompleteCount:", orderCompleteCount)
    print("paymentCompleteCount:", paymentCompleteCount)
    print("processCompleteCount:", processCompleteCount)


        #--------------------------------------------------------------------------------------------------
def main():
    run_sim(5,5,100) #q1 is infinite, q2, q3, stop

if __name__ == "__main__":
    main()