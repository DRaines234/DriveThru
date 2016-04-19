__author__ = 'Derek'

import heapq

class EventLIst:
    heap = []
    heapq.heapify(heap) # create an empty list and convert it to a heap

    def getNextEvent(self):
        return heapq.heappop(self.heap) # gets us the first lowest element of the heap

    def scheduleEvent(self, event):
        heapq.push(self.heap, event) # put the event into the event list
