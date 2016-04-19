__author__ = 'Derek and Spencer'

import OrderQueue
import PaymentWindow
import PickupWindow
import rngs

order = OrderQueue()
payment = PaymentWindow()
pickup = PickupWindow()

def run_sim(orderQueueSize, payQueueSize, pickupQueueSize):
    order.set_max = orderQueueSize
    payment.set_max = payQueueSize
    pickup.set_max = pickupQueueSize

    #currently without any intake from data

    #check if queue is empty, then add to the queue for order window
    if order.get_queue_size < order.get_max:
        order.add_to_queue

    #check if queue is empty, then add to the queue for payment window
    if payment.get_queue_size < payment.get_max:
        payment.add_to_queue

    #check if queue is empty, then add to the queue for pickup window
    if pickup.get_queue_size < pickup.get_max:
        pickup.add_to_queue

def main():
    run_sim(5,5,5)

if __name__ == "__main__":
    main()