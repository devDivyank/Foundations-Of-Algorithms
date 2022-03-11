"""
file: oneDup.py
description: CSCI-665.04 - HMWK1: Q3 Finding the duplicate value in a sorted array
language: python3
author: Divyank Kulshrestha, dk9924
author: Advit Sharma, as3272
"""

def findDup(numList: list, dupNum = None):
    """
        implementation of the Gale-Shapley algorithm to find stable matching between two groups

        :param numList: sorted list with a duplicate value
        :param dupNum: variable to store the duplicate value
    """
    # base case
    if len(numList) < 2:
        return dupNum
    # If length is 2, checking if both elements are duplicates
    elif len(numList) == 2:
        if numList[0] == numList[1]:
            dupNum = numList[0]
    else:
        # finding the middle point of the list
        mid = len(numList) // 2
        # checking if the two numbers at the middle point are duplicates
        if numList[mid-1] == numList[mid]:
            dupNum = numList[mid-1]
        else:
            # dividing the list into two parts at mid-point and making recursive calls on left and right sub-lists
            dupNum = findDup(numList[:mid], dupNum)
            dupNum = findDup(numList[mid:], dupNum)
    return dupNum

if __name__ == '__main__':
    n = int(input())
    numList = []
    for i in range(n+2):
        numList.append(int(input()))
    print(findDup(numList))
