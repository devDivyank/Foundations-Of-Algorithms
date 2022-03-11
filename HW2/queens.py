"""
file: queens.py
description: CSCI-665.04 - HMWK2: Q5 Checking if the queens' placement is valid
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""

class queens:

    def validArragement(self, queensList):
        """
            Checks if the placement of queens is valid on chessboard

            :param queensList: List of all queen-positions
        """

        '''lists to track if row/column/diagonal is blocked.
        index corresponds to the row/column/diagonal on the chessboard'''
        blockedRows=[False]*(n+1)                   # --> Complexity: O(n)
        blockedCol=[False]*(n+1)                    # --> Complexity: O(n)
        blockedLdiag=[False]*(n+1)*2                # --> Complexity: O(n)
        blockedRdiag=[False]*(n+1)*2                # --> Complexity: O(n)

        for queen in queensList:                          # --> Complexity: O(n)
            row = int(queen[0])
            col = int(queen[1])
            # if current queen's row or column or diagonal is already blocked
            if blockedRows[row] or blockedCol[col] or blockedLdiag[row+col] or blockedRdiag[n-(row-col)]:
                return "NO"
            # we block the current queen's row/column/diagonal by flipping the boolean at that index
            else:
                blockedRows[row]=True                   # --> Complexity: O(1)
                blockedCol[col]=True                    # --> Complexity: O(1)
                blockedLdiag[row + col]=True            # --> Complexity: O(1)
                blockedRdiag[n-(row - col)]=True        # --> Complexity: O(1)

        return "YES"

if __name__ == '__main__':
    n = int(input())
    queensList = []
    for _ in range(n):
        queensList.append(input().strip().split())
    obj = queens()
    print(obj.validArragement(queensList))
