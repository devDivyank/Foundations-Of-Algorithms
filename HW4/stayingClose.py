"""
file: stayingClose.py
description: CSCI-665.04 - HMWK4: Q5 - the maximum sum possible of a subsequence of A such that there exists
                                    a subsequence of B that includes the same number of elements (not necessarily
                                    corresponding to the same indices), has the same sum, and for which the partial
                                    sums of the elements of A subsequence never differ by more than one from the
                                    corresponding partial sums of the elements of the B subsequence.
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""

class stayingClose:
    def sumOfMax(self,n,A,B):
        memo = []
        # Filling memo array with lists [0,0]
        for i in range(n + 1):
            temp = []
            for j in range(n + 1):
                temp.append([0, 0])
            memo.append(temp.copy())

        #Iterating thorugh A and B lists to populate memo array
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                #Getting cumulative partial difference
                PartialDiff = B[j - 1] - A[i - 1] + memo[i - 1][j - 1][1]

                left=memo[i - 1][j]
                down=memo[i][j - 1]
                diag=memo[i - 1][j - 1]
                #Storing which among left or down values is bigger
                if left[0]>down[0]:
                    greater=left
                else:
                    greater = down

                # If Partial difference is in range
                if PartialDiff > -2 and PartialDiff < 2:
                    # If left or Down value is greator than Diagonal calculation
                    if diag[0]+B[j - 1]<greater[0]:
                        memo[i][j][0]=greater[0]
                        memo[i][j][1]=greater[1]

                    # If left or Down value is equal to Diagonal calculation
                    elif (diag[0]+B[j - 1])==greater[0]:
                        if greater[1]<PartialDiff:
                            memo[i][j][0] = greater[0]
                            memo[i][j][1] = greater[1]
                        else:
                            memo[i][j][0] = diag[0] + B[j - 1]
                            memo[i][j][1] = PartialDiff
                    else:
                        memo[i][j][0] = memo[i - 1][j - 1][0] + B[j - 1]
                        memo[i][j][1] = PartialDiff

                # If Partial difference is not in range
                else:
                    #If first value of left and down lists are same
                    if memo[i][j - 1][0] == memo[i - 1][j][0]:
                        if A[i - 1] > A[i - 2]:
                            memo[i][j][0] = memo[i][j - 1][0]
                            memo[i][j][1] = memo[i][j - 1][1]
                        else:
                            memo[i][j][0] = memo[i - 1][j][0]
                            memo[i][j][1] = memo[i - 1][j][1]

                    # If first value of down lists is greator
                    elif memo[i][j - 1][0] > memo[i - 1][j][0]:
                        memo[i][j][0] = memo[i][j - 1][0]
                        memo[i][j][1] = memo[i][j - 1][1]

                    # If first value of left lists is greator
                    else:
                        memo[i][j][0] = memo[i - 1][j][0]
                        memo[i][j][1] = memo[i - 1][j][1]

        # Checking if such a subsequnce exists or not
        if memo[n][n][1] == 0:
            return memo[n][n][0]
        else:
            return 0

if __name__ == '__main__':
    n=int(input())
    obj=stayingClose()
    A = []

    #Converting String to int array
    valuesA = input().strip().split()
    valuesB=input().strip().split()

    # Populating lists based on input
    for i in range(n):
        point = valuesA[i]
        A.append(int(point))

    B = []
    for i in range(n):
        point = valuesB[i]
        B.append(int(point))

    print(obj.sumOfMax(n,A,B))