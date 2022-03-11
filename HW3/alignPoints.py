"""
file: alignPoints.py
description: CSCI-665.04 - HMWK2: Q4 - maximum pair of points that can be aligned
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""

class alignPoints:
    
    def maxAlign(self, allPoints: list):
        """
            calculates the occurrences of perpendicular bisectors, sorts and counts the occurrences in an array
            to returns the count of the maximum-occurring line, which is equivalent
            the maximum pair of points that will align.

            :param allPoints: a list of all points as tuple (x-coordinate, y-coordinate)
        """
        # gets all the perpendicular bisectors
        pbOfPairs = self.getPerpendicularBisectors(allPoints)             # --> Complexity: O(n^2)

        # sorts the array of all perpendicular bisectors
        pbOfPairs = self.sortPerpendiculars(pbOfPairs)                    # --> Complexity: O(nlogn)

        # counts the occurrences of the maximum-occurring perpendicular bisector
        currCount = 1
        lastVal = pbOfPairs[0]
        maxCount = 0

        for line in pbOfPairs[1:]:                                      # --> Complexity: O(n)
            if line == lastVal:
                currCount += 1
                curr.append(line)
            else:
                if maxCount<currCount:
                    maxCount=currCount
                    curr = []
                currCount = 1
            lastVal = line

        return max(maxCount, currCount)

    def getPerpendicularBisectors(self, allPoints: list):
        """
            calculates and returns the slope and y-intercept of all the
            perpendicular bisectors as tuple in a list

            :param allPoints: a list of all points as tuple (x-coordinate, y-coordinate)
        """
        n = len(allPoints)
        allPerpendiculars = []

        # two loops to consider a pair of points at a time, for all possible combinations
        for i in range(n-1):                                            # --> Complexity: O(n^2)
            p1 = allPoints[i]
            for j in range(i+1, n):
                p2 = allPoints[j]
                if p1 == p2:
                    continue
                # midpoint of the two points
                midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                #slope of the line between two points
                try:
                    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
                except:
                    slope = None

                # if the line between the two points is vertical
                if slope == None:
                    perpendicularSlope = 0
                    perpendicularIntercept = midpoint[1]
                # if the line between the two points is horizontal
                elif slope == 0:
                    perpendicularSlope = float('inf')
                    perpendicularIntercept = midpoint[0]
                else:
                    perpendicularSlope = -1 / slope
                    perpendicularIntercept = midpoint[1] - (perpendicularSlope * midpoint[0])

                perpendicularLine = (perpendicularSlope, perpendicularIntercept)
                allPerpendiculars.append(perpendicularLine)                 # --> Complexity: O(1)

        # a list of all the perpendicular bisectors
        return allPerpendiculars

    def sortPerpendiculars(self, allPerpendiculars):
        """
            sorts the list of all perpendicular bisectors using merge sort      # --> Complexity: O(nlogn)

            :param allPerpendiculars: a list of all perpendiculars as tuple (slope, y-intercept)
        """
        if len(allPerpendiculars) == 1:
            return allPerpendiculars

        mid = int(len(allPerpendiculars) / 2)
        leftList = self.sortPerpendiculars(allPerpendiculars[0:mid])
        rightList = self.sortPerpendiculars(allPerpendiculars[mid:])

        # merges the two lists in order
        merged = self.mergeLists(leftList, rightList)                           # --> Complexity: O(n)
        return merged

    def mergeLists(self, lA, lB):
        """
            merges two lists in a sorted order

            :param lA: first list
            :param lB: second list
        """
        left = 0
        right = 0
        lenA = len(lA)
        lenB = len(lB)
        output = []
        count = 0
        while left < lenA and right < lenB:                                 # --> Complexity: O(n)
            if self.compare(lA[left], lB[right]) == 1:
                output.append(lA[left])
                left += 1
            else:
                output.append(lB[right])
                right += 1
                count += lenA - left

        if left < lenA:
            while left < lenA:                                              # --> Complexity: O(n)
                output.append(lA[left])
                left += 1
        else:
            while right < lenB:                                             # --> Complexity: O(n)
                output.append(lB[right])
                right += 1
                count += lenA - left

        return output

    def compare(self, member1, member2):
        """
            compare function to sort the perpendiculars based on slope and
            intercept values, used in the mergesort function

            :param member1: first perpendicular
            :param member2: second perpendicular
        """
        slope1 = member1[0]
        intercept1 = member1[1]
        slope2 = member2[0]
        intercept2 = member2[1]

        if slope1 > slope2:
            return 2
        elif slope1 == slope2:
            if intercept1 > intercept2:
                return 2
            else:
                return 1
        else:
            return 1

if __name__ == '__main__':
    obj = alignPoints()
    n = int(input())
    allPoints = []

    # storing all the points in an array as tuple (x-coordinate, y-coordinate)
    for _ in range(n):
        point = input().strip().split()
        allPoints.append((int(point[0]), int(point[1])))

    # prints the maximum number of pairs that align
    print(obj.maxAlign(allPoints))                                  # --> Overall complexity: O(n^2)