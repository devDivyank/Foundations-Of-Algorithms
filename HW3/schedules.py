"""
file: schedules.py
description: CSCI-665.04 - HMWK3: Q5 Count of different possible schedules
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""
import math

class schedules:

    def schedule_60_90(self, n):                                        # --> Complexity: O(1)
        """
            CASE 1 - returns the number of schedules for 'n' hours, lectures starting after fixed times

            :param n: number of hours to schedule for
        """
        rem = n % 3
        quotient = math.floor(n / 3)
        result = int(math.pow(13, quotient))
        if rem == 2:
            return result * 5
        elif rem == 1:
            return result * 2
        else:
            return result

    def thirtyMin(self, n, computedValues):                         # --> Complexity: O(n)
        """
            CASE 2 - returns the number of schedules for 'n' hours, lecture starting every 30 mins

            :param n: number of hours to schedule for
            :param computedValues: a list to store previous values
        """
        # base cases, when hour(s) = 0, 1, 2, 3
        if n == 0:
            return 0
        elif n == 1:
            return 1
        elif n == 2:
            return 2
        elif n == 3:
            return 4
        # if value not computed before
        elif computedValues[n] != 0:
            return computedValues[n]
        # recurrence to compute value for n'th hour - S[n] = S[n-1] + S[n-2] + S[n-3]
        else:
            computedValues[n] = self.thirtyMin(n - 1, computedValues) + \
                                self.thirtyMin(n - 2, computedValues) + \
                                self.thirtyMin(n - 3, computedValues)
            return computedValues[n]
            

if __name__ == '__main__':
    obj = schedules()
    n = int(input())
    computedValues = [0] * (n*2+1)
    # output for CASE-1
    print(obj.schedule_60_90(n))
    # output for CASE-2
    print(obj.thirtyMin(n*2, computedValues))
