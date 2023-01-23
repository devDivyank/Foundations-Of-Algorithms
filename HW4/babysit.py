"""
file: babysit.py
description: CSCI-665.04 - HMWK4: Q4 Job for max income
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""


class babysit:

    #Sorting by day and job end time
    def sortbyDaysNTime(self, jobs):
        if len(jobs) == 1:
            return jobs

        mid = int(len(jobs) / 2)
        leftList = self.sortbyDaysNTime(jobs[0:mid])
        rightList = self.sortbyDaysNTime(jobs[mid:])

        merged = self.mergeLists(leftList, rightList)
        return merged

    # Helper function to merge lists
    def mergeLists(self, lA, lB):
        left = 0
        right = 0
        lenA = len(lA)
        lenB = len(lB)
        output = []
        count = 0
        while left < lenA and right < lenB:
            if self.compare(lA[left], lB[right]) == 1:
                output.append(lA[left])
                left += 1
            else:
                output.append(lB[right])
                right += 1
                count += lenA - left

        if left < lenA:
            while left < lenA:
                output.append(lA[left])
                left += 1
        else:
            while right < lenB:
                output.append(lB[right])
                right += 1
                count += lenA - left
        return output

    # Helper function to compare two jobs
    def compare(self, member1, member2):
        if member2[0] > member1[0]:
            return 1
        elif member1[0] == member2[0]:
            if member1[2] < member2[2]:
                return 1
            else:
                return 2
        else:
            return 2

    # Function to calculate phi , need for interval scheduling
    def phi(self, n, jobs):
        end = jobs[n][1]

        for i in range(len(jobs)):
            if jobs[i][2] < end and jobs[i + 1][2] >= end:
                return i
        return 0

    # Separating jobs based on days
    def separateJobs(self, jobs):
        sorted_jobs = self.sortbyDaysNTime(jobs)
        day = 1
        jobs_sep_by_days = []
        jobs_in_day = []

        jobs_cnt = len(sorted_jobs)

        for i in range(jobs_cnt):
            if i == jobs_cnt - 1 or sorted_jobs[i + 1][0] != day:
                jobs_in_day.append(sorted_jobs[i])
                day += 1
                jobs_sep_by_days.append(jobs_in_day.copy())
                jobs_in_day = []
            else:
                jobs_in_day.append(sorted_jobs[i])

        return jobs_sep_by_days

    #Function to calculate maxIncome
    def getMaxIncome(self, jobs):

        n = len(jobs)

        s = []

        #Creates DP array
        for i in range(n + 1):
            temp = []
            for j in range(n + 1):
                temp.append(0)
            s.append(temp.copy())


        for i in range(n + 1):
            for j in range(n + 1):

                if i == 0:
                    if jobs[j - 1][3] >= 4:
                        s[i][j] = s[i][j - 1]
                    else:
                        s[i][j] = max(s[i][j-1], jobs[j-1][-1] + s[i][self.phi(j-1,jobs)])

                # Case when both are trying to acces the same job
                elif i == j:

                    # If children count >4 , then work together
                    if jobs[i - 1][3] >= 4:
                        s[i][j] = max((jobs[i-1][-1] + s[self.phi(i-1,jobs)][self.phi(j-1,jobs)]),
                                      s[i - 1][j - 1])

                    #Else , one of them works and other loses acces to it
                    else:
                        s[i][j] = max((jobs[i-1][-1] + s[self.phi(i-1, jobs)][j-1]),
                                      (jobs[i-1][-1] + s[i-1][self.phi(j-1,jobs)]), s[i-1][j-1])


                elif i < j:
                    # if one of them is ahead then we push other one to take the job
                    if jobs[j - 1][3] < 4:
                        s[i][j] = max(s[i][j-1], jobs[j-1][-1] + s[i][self.phi(j-1, jobs)])

                    #Since both have to take this job together , this job can't be done by brother or sister alone
                    else:
                        s[i][j] = s[i][j-1]

                # since brother and sister are equivalent , we dont need to fill half of the DP array
                elif i > j:
                    s[i][j] = s[j][i]


        return s[n][n]


if __name__ == '__main__':
    obj = babysit()
    jobs = []
    n = int(input())

    ## Creating total cost and appending it to every jobs
    for i in range(n):
        temp = input().strip().split()
        job = [int(i) for i in temp]
        job[4] = int(job[4] * ((job[2] - job[1]) / 100))

        # Exluding jobs which are beyond daily time limit
        if job[1] >= 600 and job[2] <= 2300:
            jobs.append(job)

    ## Separating jobs by days
    all_jobs = obj.separateJobs(jobs)

    ## Iterating through each day
    totalMaxIncome = 0
    for jobList in all_jobs:
        maxIncomeInDay = obj.getMaxIncome(jobList)
        totalMaxIncome += maxIncomeInDay

    print(totalMaxIncome)
