__author__ = 'Derek and Spencer'

import OrderQueue
import PaymentWindow
import PickupWindow
import rvgs
import rngs
import Event
import EventList


def get_arrival(interarrival):
    get_arrival.arrival_time += rvgs.exponential(interarrival) #adjusting this number will adjust our inter-arrival time
    return get_arrival.arrival_time # arrival time is one of those function variable things that I cant remember the name of

class stats:
    def __init__(self):
        self.processes_complete = 0
        self.total_arrivals = 0
        self.stuck_in_order_cnt = 0 #in order queue waiting for payment queue to empty
        self.stuck_in_pay_cnt = 0 #in payment queue, waiting for pickup queue to empty
        self.avg_order_cant_mv_time = 0#sum all inter stuck times and divide by stop for average stuck time PER window
        self.avg_payment_cant_mv_time = 0
        self.total_order_q_t = 0
        self.total_payment_q_t = 0
        self.total_pickup_q_t = 0
        self.order_time = 0 #time spent at order window
        self.payment_time = 0 # time spent at payment window
        self.pickup_time = 0 # time spent at pickup window
        self.real_ending = 0 #real ending time for the system

class time_structure:
    def __init__(self):
        self.arrival = -1                # next arrival time, we keep this here just so we have a running arrival
        self.current = -1                # we have to keep track of the current time

def run_sim(payQueueSize, pickupQueueSize, iterations, interarrival):
    order = OrderQueue.OrderQueue()
    payment = PaymentWindow.PaymentWindow()
    pickup = PickupWindow.PickupWindow()
    totalCars = 0
    arrivalCount = 0
    orderCompleteCount = 0
    paymentCompleteCount = 0
    processCompleteCount = 0
    totalWaitForPaymentQueue = 0
    totalWaitForPickupQueue = 0

    payment.set_max(payQueueSize)
    pickup.set_max(pickupQueueSize)
    STOP = iterations
    EL = EventList.EventList() # create a new event list object

    get_arrival.arrival_time = 0 # initialize arrival time to 0


    t = time_structure()
    return_stats = stats()
    t.current = 0 # set the simulation clock to 0

    arrival = Event.Event() # create a new event object
    t.arrival = get_arrival(interarrival) # get our first arrival time, we might get rid of this
    arrival.time = t.arrival # set the objects time to t.arrival
    arrival.eventType = Event.eventType(1) # set the enum to make the event type be an arrival
    EL.scheduleEvent(arrival) # add the arrival to the event list.
    arrivalCount += 1

    # We do not need to set the completions to infinity because it is the same as the objects not existing.



    #currently without any intake from data

    while(t.arrival < STOP or (order.get_queue_size() + payment.get_queue_size() + pickup.get_queue_size()) > 0): # keep running the simulation until we reach our stop time
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
                service = order.get_service()
                orderComplete.time = t.current + service #calculate service time and add it to curr time to get completion time
                EL.scheduleEvent(orderComplete) #add to event list
                order.order_complete() #removes a car from the order queue
                orderCompleteCount += 1
                payment.add_to_queue() #adds the car to the payment window
                return_stats.order_time += service # time leaving the order window
            else:
                moveOrder = Event.Event()
                moveOrder.eventType = Event.eventType(5) # register event as move order car event
                service = order.get_service()
                moveOrder.time = t.current + service # we will still calculate the service time as if we were completing
                EL.scheduleEvent(moveOrder)#add to event list
                return_stats.order_time += service #scheduling a move order but we are still in the order queue

            #schedule next arrival
            if t.current < STOP: # if we are still below our stop time, schedule another arrival
                arrival = Event.Event()
                t.arrival = get_arrival(interarrival)
                arrival.time = t.arrival
                arrival.eventType = Event.eventType(1) #set this event as an type arrival
                EL.scheduleEvent(arrival) #add arrival to event list
                #print("arrival", t.current)
                arrivalCount += 1

        #process order completion
        elif event.eventType.value == 2:
            # check if payment window has room
            if pickup.get_queue_size() < pickup.get_max():
                paymentComplete = Event.Event()
                paymentComplete.eventType = Event.eventType(3) #register it as a payment complete
                service = payment.get_service()
                paymentComplete.time = t.current + service
                EL.scheduleEvent(paymentComplete) #add to event list
                payment.pay_complete() #remove  from payment window
                paymentCompleteCount += 1
                pickup.add_to_queue() # add car to pickup queue
                return_stats.payment_time += service # add service time to payment total time
                #print("order complete", t.current)

            else:
                paymentMove = Event.Event()
                paymentMove.eventType = Event.eventType(6) # register this event as a payment move event
                service = payment.get_service()
                paymentMove.time = t.current + service #add time as if we were processing a completion
                EL.scheduleEvent(paymentMove)#add to event list
                return_stats.payment_time += service # add the service time for the scheduled wait because we are still at the window

        #payment completion
        elif event.eventType.value == 3:

            pickupComplete = Event.Event()
            pickupComplete.eventType = Event.eventType(4) #register it as a pickup completion
            service = pickup.get_service()
            pickupComplete.time = t.current + service
            EL.scheduleEvent(pickupComplete) # add to event list
            return_stats.pickup_time += service #add to total time for pickup
            #print("payment complete", t.current)


        #process pickup
        elif event.eventType.value == 4:

            pickup.pickup_complete() #remove car from pickup
            #print("pickup complete", t.current)
            processCompleteCount += 1
            #no time needed here

        # process move order car event, works same as order complete, just later on
        elif event.eventType.value == 5:
            totalWaitForPaymentQueue += 1
            #print("move order = ", t.current)
            if payment.get_queue_size() < payment.get_max(): #if there's room in the next queue
                orderComplete = Event.Event()
                orderComplete.eventType = Event.eventType(2) # register event as an order complete
                orderComplete.time = t.current #if there is room, schedule the order completion now
                EL.scheduleEvent(orderComplete) #add event to event list
                order.order_complete() #removes a car from the order queue
                orderCompleteCount += 1
                payment.add_to_queue() #adds the car to the payment window
                #we already added the time for this event when we created it. The completion here gets scheduled for right now
            # if next window is full, make another can order move event.
            else:
                moveOrder = Event.Event()
                moveOrder.eventType = Event.eventType(5) # register event as move order car event
                delay = rvgs.random()
                moveOrder.time = t.current + delay # not totally sure if this is appropriate here
                return_stats.avg_order_cant_mv_time += service #add just the reschedule time
                EL.scheduleEvent(moveOrder)#add to event list
                return_stats.order_time +=  delay #we are stuck in the orde queue so add this time to its time

        #process move payment car event works the same as the payent completion, just later
        elif event.eventType.value == 6:
            totalWaitForPickupQueue += 1
            if pickup.get_queue_size() < pickup.get_max(): # if there's room in the next queue
                paymentComplete = Event.Event()
                paymentComplete.eventType = Event.eventType(3) #register as a payment completion event
                paymentComplete.time = t.current # if there's room in the queue, schedule a payment completion now
                EL.scheduleEvent(paymentComplete) # add event to event list
                payment.pay_complete() #remove  from payment window
                paymentCompleteCount += 1
                pickup.add_to_queue() # add car to pickup queue
                #we already added the time for this event when scheduling it.
                #if next window is full schedule another
            else:
                paymentMove = Event.Event()
                paymentMove.eventType = Event.eventType(6) #register as a payment move event
                delay = rvgs.random()
                paymentMove.time = t.current + service #not really sure if this is appropriate time to check again
                return_stats.avg_payment_cant_mv_time += service #add just the reschedule time
                EL.scheduleEvent(paymentMove) #add it to the event list
                return_stats.payment_time += delay #we are still stuckin in the service time for this

    #print("total non avg'd payment time = ", return_stats.payment_time)

    return_stats.processes_complete = processCompleteCount
    return_stats.total_arrivals = arrivalCount
    return_stats.stuck_in_order_cnt = totalWaitForPaymentQueue
    return_stats.stuck_in_pay_cnt = totalWaitForPickupQueue
    return_stats.avg_order_cant_mv_time = (return_stats.avg_order_cant_mv_time / t.current) / orderCompleteCount
    return_stats.avg_payment_cant_mv_time = (return_stats.avg_payment_cant_mv_time / t.current) / paymentCompleteCount
    return_stats.order_time = return_stats.order_time / orderCompleteCount# / totalCars #gets average time per car
    return_stats.payment_time = return_stats.payment_time / paymentCompleteCount# / totalCars #gets average time per car
    return_stats.pickup_time = return_stats.pickup_time / processCompleteCount# / totalCars #gets average time per car
    return_stats.real_ending = t.current
    #print(processCompleteCount)
    #print("totalCars:", totalCars)
    # print("arrivalCount:", arrivalCount)
    # print("orderCompleteCount:", orderCompleteCount)
    #print("paymentCompleteCount:", paymentCompleteCount)
    # print("processCompleteCount:", processCompleteCount)
    # print("largest order queue: ", order.getLargestSize())
    # print("largest payment queue: ", payment.getLargestSize())
    # print("largest pickup queue: ", pickup.getLargestSize())
    # print("Number of waiting for payment Queue to open:", totalWaitForPaymentQueue)
    # print("Number of waiting for pickup Queue to open:", totalWaitForPickupQueue)
    # print(processCompleteCount/arrivalCount)
    #print("avg order takes ", return_stats.order_time)
    #print("avg payment takes ", return_stats.payment_time)
    #print("avg pickup takes ", return_stats.pickup_time)
    #print("time = ",t.current)
    return return_stats

        #--------------------------------------------------------------------------------------------------
def main():
    #rngs.put_seed(0) # for more randomization optimization
    q1 = 2
    q2 = 10
    iterations = 60
    interarrival = 1.0
    monte_rounds = 500
    sum_processes_complete = 0
    sum_total_arrivals = 0
    sum_stuck_in_order_cnt = 0 #in order queue waiting for payment queue to empty
    sum_stuck_in_pay_cnt = 0 #in payment queue, waiting for pickup queue to empty
    sum_avg_order_cant_mv_time = 0#sum all geometric inter stuck times and divide by stop for average stuck time PER window
    sum_avg_payment_cant_mv_time = 0
    sum_total_order_q_t = 0
    sum_total_payment_q_t = 0
    sum_total_pickup_q_t = 0
    sum_percent_complete = 0
    '''
    for i in range(1, monte_rounds):
        stats = run_sim(q1, q2, iterations, interarrival) #q1 is infinite, q2, q3, stop
        sum_total_arrivals += stats.total_arrivals
        sum_processes_complete += stats.processes_complete
        sum_stuck_in_order_cnt += stats.stuck_in_order_cnt
        sum_stuck_in_pay_cnt += stats.stuck_in_pay_cnt
        sum_percent_complete += stats.processes_complete/stats.total_arrivals
        sum_avg_order_cant_mv_time += stats.avg_order_cant_mv_time
        sum_avg_payment_cant_mv_time += stats.avg_payment_cant_mv_time
        sum_total_order_q_t += stats.order_time
        sum_total_payment_q_t += stats.payment_time
        sum_total_pickup_q_t += stats.pickup_time



    print("total arrivals" , sum_total_arrivals/monte_rounds)
    print("total complete", sum_processes_complete/monte_rounds)
    print("stuck in order count ", sum_stuck_in_order_cnt/monte_rounds)
    print("stuck in payment count ", sum_stuck_in_pay_cnt/monte_rounds)
    print("percent complete ", sum_percent_complete/monte_rounds)
    print("average order window backup:", sum_avg_order_cant_mv_time / monte_rounds)
    print("average payment window backup: ", sum_avg_payment_cant_mv_time / monte_rounds)
    print("average time per car in in order queue: ", sum_total_order_q_t / monte_rounds)
    print("average time per car in payment queue: ", sum_total_payment_q_t / monte_rounds)
    print("average time per car in pickup queue: ", sum_total_pickup_q_t / monte_rounds)
    print("total time in system: ", (sum_total_order_q_t / monte_rounds) + (sum_total_order_q_t / monte_rounds) + (sum_total_pickup_q_t / monte_rounds))
        #print(" ")



    #run_sim(q1, q2, iterations)
    '''
    q1A = []
    q2A = []
    order_time  = []
    payment_time = []
    pickup_time = []
    totals = []


    for i in range(0,9):
        #reset sums to 0
        order_stuck_sum = 0
        payment_stuck_sum = 0
        total_time_sum = 0
        time_at_order_sum = 0
        time_at_payment_sum = 0
        time_at_pickup_sum = 0
        avg_real_ending_time = 0

        for j in range(0,10):
            stats = run_sim(q1,q2,iterations, interarrival)
            #add the sums up
            time_at_order_sum += stats.order_time
            time_at_payment_sum += stats.payment_time
            time_at_pickup_sum += stats.pickup_time
            total_time_sum += stats.order_time + stats.payment_time + stats.pickup_time
            avg_real_ending_time += stats.real_ending

        #add to lists to make for easy exceling
        q1A.append(q1)
        q2A.append(q2)
        order_time.append(time_at_order_sum / j)
        payment_time.append(time_at_payment_sum / j)
        pickup_time.append(time_at_pickup_sum / j)
        totals.append(total_time_sum / j)
        #calculate average and print result
        '''
        print("payment window size = ", q1)
        print("pickup window size = ", q2)
        print("average time stuck at order window = ", time_at_order_sum / j)
        print("average time stuck at payment window= ", time_at_payment_sum / j)
        print("average time stuck in pickup window = ", time_at_pickup_sum / j)
        print("average total time in drive thru = ", total_time_sum / j)
        #print("average ending time = ", avg_real_ending_time / j)
        print(" ")
        '''
        # change queue sizes to calculate the next round
        q1 += 1
        q2 -= 1

    print("q1")
    for stat in q1A:
        print(stat)

    print("-----------------")
    print("q2")
    for stat in q2A:
        print(stat)

    print("-----------------")
    print("order time")
    for stat in order_time:
        print(stat)

    print("-----------------")
    print("payment time")
    for stat in payment_time:
        print(stat)

    print("-----------------")
    print("pickup time")
    for stat in pickup_time:
        print(stat)

    print("-----------------")
    print("average total time")
    for stat in totals:
        print(stat)


if __name__ == "__main__":
    main()