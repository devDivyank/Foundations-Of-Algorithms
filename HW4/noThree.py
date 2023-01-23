"""
file: noThree.py
description: CSCI-665.04 - HMWK4: Q2 find a subsequence with the maximum possible sum, with the restriction
                            that we are not allowed to take three con- secutive elements from the original sequence.
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""

class NoThree:

    #Function to fill DP array
    def largestSum(self,arr):
        n=len(arr)

        # Creating list to values obtained from recurrence
        inc=[0]*n
        inc[0]=arr[0]
        inc[1]=arr[0]+arr[1]

        notInc = [0] * n
        notInc[0]=0
        notInc[1]=inc[0]

        for i in range(2,len(arr)):
            notInc[i]=max(inc[i-1],inc[i-2])

            # checking if last element is smaller than element before it
            if arr[i-1]<arr[i-2]:
                inc[i]=arr[i]+notInc[i-1]
            else:
                inc[i] = arr[i] + arr[i-1] + notInc[i - 2]

        return inc

if __name__ == '__main__':
    obj = NoThree()
    n = int(input())
    arr = []
    values=input().strip().split()
    for i in range(n):
        point = values[i]
        arr.append(int(point))

    print(max(obj.largestSum(arr)))