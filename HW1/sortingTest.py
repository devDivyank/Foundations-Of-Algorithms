"""
file: sortingTest.py
description: CSCI 665 Section 4 - HMWK1: Q5 Implement Merge Sort, Insertion Sort, Bucket Sort and test inputs
language: python3
author: Divyank Kulshrestha, dk9924
author: Advit Sharma, as3272
"""

import random
# Module used for randomizing input values

import time
# Module used to calculate time of execution for algorithms

def mergeSort(numList: list):
    '''
        Implementation of Merge Sort

        :param numList: List of inputs
        :return: sorted list
    '''
    # base case
    if len(numList) < 2:
        return numList
    else:
        # dividing the list into two parts at mid-point and making recursive calls on left and right sub-lists
        mid = len(numList) // 2
        left = mergeSort(numList[:mid])
        right = mergeSort(numList[mid:])

        # combining the sorted left and right sublists
        sortedList = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                sortedList.append(left[i])
                i += 1
            else:
                sortedList.append(right[j])
                j += 1
        if i < len(left):
            sortedList.extend(left[i:])
        if j < len(right):
            sortedList.extend(right[j:])
        return sortedList

def insertionSort(numList: list):
    '''
        Implementation for Insertion Sort

        :param numList: List of Inputs
        :return: sorted List
    '''
    timer = time.time()
    # running a loop from 1 to (length of list-1)
    i = 1
    while i < len(numList):
        if (time.time() - timer) > 15:
            return False
        # loop from i to 1
        j = i
        while j > 0 and numList[j-1] > numList[j]:
            # swapping the j'th and (j-1)'th element if not in correct order amongst them
            numList[j - 1], numList[j] = numList[j], numList[j-1]
            j -= 1
        i += 1
    return numList

def bucketSort(numList: list):
    '''
        Implementaion of Bucket Sort

        :param numList: List of Inputs
        :return: sorted list
    '''
    timer = time.time()
    n = len(numList)
    buckets = []
    # creating a bucket of size equal to length of numList
    for _ in range(n):
        buckets.append([])
    # assigning values to appropriate buckets
    for num in numList:
        index = int(n * num)
        buckets[index].append(num)
    # calling insertion sort on every bucket
    for i in range(n):
        if (time.time()-timer) > 15:
            return False
        buckets[i] = insertionSort(buckets[i])
    # combining the buckets to get the fully sorted list
    k = 0
    for i in range(n):
        for j in range(len(buckets[i])):
            numList[k] = buckets[i][j]
            k += 1
    return numList

def calculateTime(sortingAlgo, input):
    '''
        Function to calculate time

        :param sortingAlgo: Takes input of function for sorting algorithm
        :param input: input for sorting algorithm
        :return:
    '''
    begin = time.time()                     # starting time
    timeLimit = sortingAlgo(input)
    end = time.time()                       # ending time
    x = end - begin                         # calculating time of execution for algorithm
    return False if not timeLimit else x

if __name__ == '__main__':

    #Input lists for different input size and distributions
    numList100uniform = []
    numList1000uniform = []
    numList10000uniform = []
    numList100000uniform = []
    numList100normal = []
    numList1000normal = []
    numList10000normal = []
    numList100000normal = []
    for i in range(0,100):
        numList100uniform.append(random.uniform(0,1))               # uniform function is used for uniform distribution
        numList100normal.append(random.gauss(0.5, 0.00001))         # gauss function is used for normal distribution
    for i in range(0,1000):
        numList1000uniform.append(random.uniform(0,1))
        numList1000normal.append(random.gauss(0.5, 0.00001))
    for i in range(0,10000):
        numList10000uniform.append(random.uniform(0,1))
        numList10000normal.append(random.gauss(0.5, 0.00001))
    for i in range(0,100000):
        numList100000uniform.append(random.uniform(0,1))
        numList100000normal.append(random.gauss(0.5, 0.00001))

    #running test cases
    test_cases_uniform = [numList100uniform, numList1000uniform, numList10000uniform, numList100000uniform]
    print("UNIFORM DISTRIBUTION: ")
    size = 100
    for x in test_cases_uniform:
        print("Time for Merge sort on input size of " + str(size) + " uniformly distributed ran for "
              + str("more than 3 minutes" if not calculateTime(mergeSort, x) else calculateTime(mergeSort, x)))
        print("Time for Insertion sort on input size of " + str(size) + " uniformly distributed ran for "
              + str("more than 3 minutes" if not calculateTime(insertionSort, x) else calculateTime(insertionSort, x)))
        print("Time for Bucket sort on input size of " + str(size) + " uniformly distributed ran for "
              + str("more than 3 minutes" if not calculateTime(bucketSort, x) else calculateTime(bucketSort, x)))
        size = size*10

    test_cases_normal = [numList100normal, numList1000normal, numList10000normal, numList100000normal]
    print("\n\nGAUSSIAN DISTRIBUTION: ")
    size = 100
    for x in test_cases_normal:
        print("Time for Merge sort on input size of " + str(size) + " Gaussian distributed ran for "
              + str("more than 3 minutes" if not calculateTime(mergeSort, x) else calculateTime(mergeSort, x)))
        print("Time for Insertion sort on input size of " + str(size) + " Gaussian distributed ran for "
              + str("more than 3 minutes" if not calculateTime(insertionSort, x) else calculateTime(insertionSort, x)))
        print("Time for Bucket sort on input size of " + str(size) + " Gaussian distributed ran for " +
              str("more than 3 minutes" if not calculateTime(bucketSort, x) else calculateTime(bucketSort, x)))
        size = size*10