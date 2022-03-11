"""
file: boss.py
description: CSCI-665.04 - HMWK2: Q4 Completing tasks within the deadline
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779

Heap implementation: from previous course CSCI-603: Computational Problem Solving
"""

class Heap(object):
    '''
    Heap that orders by a given comparison function, default to less-than.
    '''
    __slots__ = ('data', 'size', 'lessfn')

    def __init__(self, lessfn):
        '''
        Constructor takes a comparison function.
        :param lessfn: Function that takes in two heap objects and returns true
        if the first arg goes higher in the heap than the second
        '''
        self.data = []
        self.size = 0
        self.lessfn = lessfn

    def __parent(self, loc):
        '''
        Helper function to compute the parent location of an index
        :param loc: Index in the heap
        :return: Index of parent
        '''
        return (loc - 1) // 2

    def __bubbleUp(self, loc):
        '''
        Starts from the given location and moves the item at that spot
        as far up the heap as necessary
        :param loc: Place to start bubbling from
        '''
        while loc > 0 and \
                self.lessfn(self.data[loc], self.data[self.__parent(loc)]):
            self.data[loc], self.data[self.__parent(loc)] = \
                self.data[self.__parent(loc)], self.data[loc]
            loc = self.__parent(loc)

    def __bubbleDown(self, loc):
        '''
        Starts from the given location and moves the item at that spot
        as far down the heap as necessary
        :param loc: Place to start bubbling from
        '''
        swapLoc = self.__smallest(loc)
        while swapLoc != loc:
            self.data[loc], self.data[swapLoc] = \
                self.data[swapLoc], self.data[loc]
            loc = swapLoc
            swapLoc = self.__smallest(loc)

    def __smallest(self, loc):
        '''
        Finds the "smallest" value of loc and loc's two children.
        Correctly handles end-of-heap issues.
        :param loc: Index
        :return: index of smallest value
        '''
        ch1 = loc * 2 + 1
        ch2 = loc * 2 + 2
        if ch1 >= self.size:
            return loc
        if ch2 >= self.size:
            if self.lessfn(self.data[loc], self.data[ch1]):
                return loc
            else:
                return ch1
        # now consider all 3
        if self.lessfn(self.data[ch1], self.data[ch2]):
            if self.lessfn(self.data[loc], self.data[ch1]):
                return loc
            else:
                return ch1
        else:
            if self.lessfn(self.data[loc], self.data[ch2]):
                return loc
            else:
                return ch2

    def insert(self, item):
        '''
        Inserts an item into the heap.
        :param item: Item to be inserted
        '''
        if self.size < len(self.data):
            self.data[self.size] = item
        else:
            self.data.append(item)
        self.size += 1
        self.__bubbleUp(self.size - 1)

    def pop(self):
        '''
        Removes and returns top of the heap
        :return: Item on top of the heap
        '''
        assert self.size > 0, "Popping from an empty Heap"
        retjob = self.data[0]
        self.size -= 1
        # if we are popping the only element, bubbling is unnecessary, so:
        if self.size > 0:
            self.data[0] = self.data.pop(self.size)
            self.__bubbleDown(0)
        else:
            # we are popping the last element from the heap
            self.data.pop(0)
        return retjob

class boss:
    timer=0
    tracker=0

    def canComplete(self,taskList):
        """
            checks if the tasks in the list can be completed without missing deadlines

            :param taskList: list of all the tasks
        """

        taskHeap = Heap(lambda x, y: x[1] < y[1])
        taskHeap.insert(taskList.pop(0))
        nextTask = self.getNextTask(taskList, taskHeap)

        # while there are tasks in heap or list
        while taskHeap.size > 0 or self.tracker<len(taskList) :
            # Gets next task from either list or heap
            nextTask = self.getNextTask(taskList, taskHeap)
            if self.tracker<len(taskList):
                status = self.processTaskList(taskHeap, nextTask)
                self.tracker += 1
            else:
                status = self.processTaskONHeap(nextTask)

            if status=="NO":
                return "NO"

        return "YES"


    def processTaskList(self,taskHeap,nextTask):
        """
            process' the next task obtained the list

            :param taskHeap: tasks stored based on priority
            :param nextTask: list of all remaining tasks
        """
        heapTop=taskHeap.data[0]

        if self.timer+nextTask[2]>nextTask[1]:
            return "NO"

        waitTime=nextTask[0]-self.timer
        if heapTop[1] <= nextTask[1] and heapTop[0] < nextTask[0]:
            if waitTime>0 and waitTime<heapTop[2]:
                heapTop[2]-=waitTime
                self.timer += waitTime
            elif waitTime>0 and waitTime==heapTop[2]:
                taskHeap.pop()
                self.timer += waitTime
            elif waitTime>0 and waitTime>heapTop[2]:
                self.timer += heapTop[2]
                taskHeap.pop()
        taskHeap.insert(nextTask)

    def processTaskONHeap(self,nextTask):
        """
            once tasklist is empty, all tasks on heap are processed

            :param nextTask: task left on task list, or None is task list is empty
        """

        # If heap is empty then all tasks have been processed
        if nextTask==None:
            return "YES"
        if self.timer + nextTask[2] > nextTask[1]:
            return "NO"
        self.timer+=nextTask[2]

    def getNextTask(self, taskList, taskHeap):
        """
            returns the next task from the heap or the task list

            :param taskHeap: tasks stored based on priority
            :param taskList: list of all remaining tasks
        """

        if len(taskList) == self.tracker and taskHeap.size > 0:
            return taskHeap.pop()
        if len(taskList) > self.tracker:
            task=taskList[self.tracker]
            return task
        return None

if __name__ == '__main__':
    n=int(input())
    values=[]
    for i in range(n):
        temp=input().strip().split()
        values.append([int(temp[0]),int(temp[1]),int(temp[2])])

    obj=boss()
    print(obj.canComplete(values))

