"""
file: picture.py
description: CSCI-665.04 - HMWK2: Q3 Swaps necessary to get the class into the desired order
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""

class picture:

    def countSwaps(self,values):
        temp = self.recursiveHelper(values)
        return temp[0]

    def recursiveHelper(self,values):
        """
            divides the data and then merges it (MergeSort)

            :param values: list of values to be sorted
        """
        if len(values) == 1:                                        # --> Complexity: O(1)
            return [0,values]
        # midpoint
        mid = int(len(values)/2)

        # recursive call on left half
        leftList = self.recursiveHelper(values[0:mid])              # --> Complexity: O(logn)

        # recursive call on right half
        rightList = self.recursiveHelper(values[mid:])              # --> Complexity: O(logn)

        # merges left and right halfs
        merged = self.mergeLists(leftList[1], rightList[1])         # --> Complexity: O(n)
        return [leftList[0] + rightList[0] + merged[0], merged[1]]


    def mergeLists(self, lA, lB):
        """
            Merges two lists in order

            :param lA: first list
            :param lB: second list
        """
        left = 0
        right = 0
        lenA = len(lA)
        lenB = len(lB)
        output = []
        count = 0

        # picks smaller element out of lA and lB
        while left < lenA and right < lenB:                     # --> Complexity: O(n)
            if self.compare(lA[left],lB[right])==1:
                output.append(lA[left])
                left += 1
            else:
                output.append(lB[right])
                right += 1
                count += lenA-left

        # if elements in lA still remain
        if left < lenA:                                            # --> Complexity: O(n)
            while left < lenA:
                output.append(lA[left])
                left += 1

        # if elements in lb still remain
        else:
            while  right < lenB:                                   # --> Complexity: O(n)
                output.append(lB[right])
                right += 1
                count += lenA - left

        return [count,output]

    def compare(self, member1, member2):
        """
            compares two students

            :param member1: student one
            :param member2: student two
        """

        if member1[0] == member2[0]:                    # --> Complexity: O(1)
            if member1[0] == 7:
                if member2[1] > member1[1]:
                    return 1
                else:
                    return 2
            else:
                if member2[1] < member1[1]:
                    return 1
                else:
                    return 2
        else:                                           # --> Complexity: O(1)
            if member1[0] == 7:
                return 1
            if member2[0] == 7:
                return 2
            if member1[0] == 8:
                return 2
            if member2[0] == 8:
                return 1

if __name__ == '__main__':
    n = int(input())
    value = []

    for i in range(n):
        fromUser = input().strip().split()
        value.append((int(fromUser[0]), float(fromUser[1])))

    obj = picture()
    print(obj.countSwaps(value))
