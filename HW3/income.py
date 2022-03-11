"""
file: income.py
description: CSCI-665.04 - HMWK2: Q3 top 1% income compared to bottom earners
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""
import random

class income:

    def kthlargest(self, values, k):
        """
            returns the kth largest value in a list

            :param values: a list of values
            :param k: the kth largest value to be found
        """
        # random pivot
        pivotPos = random.randint(0,len(values)-1)
        # divides the elements into 3 buckets - lesser, equal and greater values
        L, G, E = self.partition(values, values[pivotPos])
        # if k is in 'lesser' partition
        if k < len(L):
            return self.kthlargest(L, k)                                    # --> Complexity: O(n)
        elif k >= len(L) and k < (len(L) + len(E)):
            # if k is in 'equal' partition
            return values[pivotPos]
        else:
            return self.kthlargest(G, k-len(L)-len(E))

    def partition(self, values, pivot):
        """
            divides a list into three partitions

            :param values: a list of values
            :param pivot: value based on which data is partition
        """
        L=[]
        G=[]
        E=[]
        for i in values:                                                # --> Complexity: O(n)
            # if value = pivot value
            if i == pivot:
                E.append(i)
            # if value > pivot value
            elif i > pivot:
                G.append(i)
            # if value < pivot value
            else:
                L.append(i)
        return (L, G, E)

    def getTopOnePercentSum(self, incomes):
        """
            returns the combined income of top 1%

            :param incomes: a list of values
        """
        valuesLen=len(incomes)
        # value for pivot
        popu_at99=int(valuesLen*0.99)
        t1_IncomeStart=self.kthlargest(incomes, popu_at99)
        t1_Income=0
        # adding all values greater than pivot value
        for income in incomes:                                              # --> Complexity: O(n)
            if income>=t1_IncomeStart:
                t1_Income+=income
        return t1_Income

    def sumTill(self, incomes, top1p):
        """
            returns the index opto which the sum of values is just less than top 1% income

            :param incomes: a list of values
            :param top1p: combined income of top 1%
        """
        if len(incomes) == 0:
            return 0
        pivotPos = random.randint(0, len(incomes) - 1)
        L, G, E, lSum, ESum = self.partitionSum(incomes, incomes[pivotPos])
        # if top 1% income is less than pivot index
        if top1p < lSum:
            return self.sumTill(L, top1p)
        elif top1p >= lSum and top1p < (lSum+ESum):
            return len(L) + (top1p - lSum) / E[0]
        else:
            return len(L) + len(E) + self.sumTill(G, top1p-lSum-ESum)

    def partitionSum(self, values, pivot):
        """
            returns the partitions 'lesser', 'equals', 'greater' and also the sums of 'lesser' and 'greater' sums

            :param values: a list of values
            :param pivot: value at the pivot index
        """
        L = []
        G = []
        E = []
        LSum = 0
        ESum = 0
        for i in values:                                            # --> Complexity: O(n)
            if i == pivot:
                ESum+=i
                E.append(i)
            elif i > pivot:
                G.append(i)
            else:
                LSum += i
                L.append(i)
        return (L, G, E, LSum, ESum)

if __name__ == '__main__':
    obj=income()
    # number of salaries
    n = int(input())
    incomes = []
    # adding salaries into a list
    for _ in range(n):
        point = input().strip()
        incomes.append(float(point))

    top1p=obj.getTopOnePercentSum(incomes)
    output=obj.sumTill(incomes,top1p)
    top1pCount=int(len(incomes)-(len(incomes)*0.99))

    if output>=(len(incomes)-top1pCount):
        output=len(incomes)-top1pCount

    bottomPerc=(output/len(incomes))

    outputPercent=int(bottomPerc*float(100))
    print(outputPercent)
