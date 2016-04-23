__author__ = 'Derek'
#This class is to just play with the stupid heaps and enums

import heapq
from enum import Enum
import rvgs

heap = []
heapq.heapify(heap)

class eventType(Enum):
    arrival = 1
    comletion1 = 2
    completeion2 = 3



class event:
    eventType = -1
    time = -1
    def __lt__(self, other): #over rides the built in comparison method so we can specify the values to compare
        return self.time < other.time


event1 = event()
event1.time = 4
event1.eventType = eventType(1)

event2 = event()
event2.time = 3
event2.eventType = eventType(2)

event3 = event()
event3.time = 8
event3.eventType = eventType(3)

heapq.heappush(heap, event1)
heapq.heappush(heap, event2)
heapq.heappush(heap, event3)

print(heapq.heappop(heap).eventType.name) # .name gives string name of enum, .value gets the number of the enum
print(heapq.heappop(heap).eventType)
print(heapq.heappop(heap).eventType)

#Next set of things is to mess with ranges of the different distributions
total_time = 0
num_items = int(rvgs.uniform(1,6))

min = 999999999999999
max = 0
for j in range(0,1000):
    total_time = 0
    for i in range(0, num_items):
        num = rvgs.exponential(1.5)
        total_time += rvgs.exponential(1.5)
    if total_time > max:
        max = total_time
    if total_time < min:
        min = total_time
print("max = ", max)
print("min = ", min)

min = 999999999
max = 0
for k in range(0,1000):
    num = rvgs.exponential(3)
    if num > max:
        max = num
    if num < min:
        min = num
print(" ")
print("min = ", min)
print("max = ", max)
