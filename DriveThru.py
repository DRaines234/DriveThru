__author__ = 'Derek and Spencer'

import OrderQueue
import PaymentWindow
import PickupWindow
import rvgs
import rngs
import Event
import EventList

order = OrderQueue.OrderQueue()
payment = PaymentWindow.PaymentWindow()
pickup = PickupWindow.PickupWindow()


def get_arrival():
    get_arrival.arrival_time += rvgs.exponential(.50) #adjusting this number will adjust our inter-arrival time
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
    EL = EventList.EventList() # create a new event list object

    get_arrival.arrival_time = 0 # initialize arrival time to 0


    t = time_structure()
    t.current = 0 # set the simulation clock to 0

    arrival = Event.Event() # create a new event object
    t.arrival = get_arrival() # get our first arrival time, we might get rid of this
    arrival.time = t.arrival # set the objects time to t.arrival
    arrival.eventType = Event.eventType(1) # set the enum to make the event type be an arrival
    EL.scheduleEvent(arrival) # add the arrival to the event list.
    arrivalCount += 1

    # We do not need to set the completions to infinity because it is the same as the objects not existing.



    #currently without any intake from data

    while(t.arrival < STOP) or (order.get_queue_size() + payment.get_queue_size() + pickup.get_queue_size()) > 0: # keep running the simulation until we reach our stop time
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
            else:
                moveOrder = Event.Event()
                moveOrder.eventType = Event.eventType(5) # register event as move order car event
                moveOrder.time = t.current + order.get_service() # we will still calculate the service time as if we were completing
                EL.scheduleEvent(moveOrder)#add to event list

            #schedule next arrival
            if t.current < STOP: # if we are still below our stop time, schedule another arrival
                arrival = Event.Event()
                t.arrival = get_arrival()
                arrival.time = t.arrival
                arrival.eventType = Event.eventType(1) #set this event as an type arrival
                EL.scheduleEvent(arrival) #add arrival to event list
                #print("arrival", t.current)
                arrivalCount += 1

        #process order completion
        elif event.eventType.value == 2:
            order.order_complete() #removes a car from the order queue
            payment.add_to_queue() #adds the car to the payment window
            # check if payment window has room
            if pickup.get_queue_size() < pickup.get_max():
                paymentComplete = Event.Event()
                paymentComplete.eventType = Event.eventType(3) #register it as a payment complete
                paymentComplete.time = t.current + payment.get_service()
                EL.scheduleEvent(paymentComplete) #add to event list
                #print("order complete", t.current)
                orderCompleteCount += 1
            else:
                paymentMove = Event.Event()
                paymentMove.eventType = Event.eventType(6) # register this event as a payment move event
                paymentMove.time = t.current + payment.get_service() #add time as if we were processing a completion
                EL.scheduleEvent(paymentMove)#add to event list

        #payment completion
        elif event.eventType.value == 3:
            payment.pay_complete() #remove  from payment window
            pickup.add_to_queue() # add car to pickup queue
            pickupComplete = Event.Event()
            pickupComplete.eventType = Event.eventType(4) #register it as a pickup completion
            pickupComplete.time = t.current + pickup.get_service()
            EL.scheduleEvent(pickupComplete) # add to event list
            #print("payment complete", t.current)
            paymentCompleteCount += 1

        #process pickup
        elif event.eventType.value == 4:
            pickup.pickup_complete() #remove car from pickup
            #print("pickup complete", t.current)
            processCompleteCount += 1

        # process move order car event, works same as order complete, just later on
        elif event.eventType.value == 5:
            #print("move order = ", t.current)
            if payment.get_queue_size() < payment.get_max(): #if there's room in the next queue
                orderComplete = Event.Event()
                orderComplete.eventType = Event.eventType(2) # register event as an order complete
                orderComplete.time = t.current #if there is room, schedule the order completion now
                EL.scheduleEvent(orderComplete) #add event to event list
            # if next window is full, make another can order move event.
            else:
                moveOrder = Event.Event()
                moveOrder.eventType = Event.eventType(5) # register event as move order car event
                moveOrder.time = t.current + rvgs.geometric(0.2) # not totally sure if this is appropriate here
                EL.scheduleEvent(moveOrder)#add to event list

        #process move payment car event works the same as the payent completion, just later
        elif event.eventType.value == 6:
           if pickup.get_queue_size() < pickup.get_max(): # if there's room in the next queue
                paymentComplete = Event.Event()
                paymentComplete.eventType = Event.eventType(3) #register as a payment completion event
                paymentComplete.time = t.current # if there's room in the queue, schedule a payment completion now
                EL.scheduleEvent(paymentComplete) # add event to event list
                #if next window is full schedule another
           else:
                paymentMove = Event.Event()
                paymentMove.eventType = Event.eventType(6) #register as a payment move event
                paymentMove.time = t.current + rvgs.geometric(0.2) #not really sure if this is appropriate time to check again
                EL.scheduleEvent(paymentMove) #add it to the event list






    print("totalCars:", totalCars)
    print("arrivalCount:", arrivalCount)
    print("orderCompleteCount:", orderCompleteCount)
    print("paymentCompleteCount:", paymentCompleteCount)
    print("processCompleteCount:", processCompleteCount)


        #--------------------------------------------------------------------------------------------------
def main():
    #rngs.put_seed(0) # for more randomization optimization
    q1 = 2
    q2 = 2
    iterations = 100

    for i in range(2, 20, 2):
        run_sim(q1, q2, iterations) #q1 is infinite, q2, q3, stop
        q1 += 2
        q2 += 2
        print(" ")

if __name__ == "__main__":
    main()