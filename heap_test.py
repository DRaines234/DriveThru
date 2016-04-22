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

for i in range(0,10):
    print(rvgs.geometric(0.1))
