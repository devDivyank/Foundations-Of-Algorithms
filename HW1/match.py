"""
file: match.py
description: CSCI-665.04 - HMWK1: Q4 Checking if more than one stable matching is possible
language: python3
author: Divyank Kulshrestha, dk9924
author: Advit Sharma, as3272
"""

from copy import deepcopy

def stableMatch(groupOne, groupTwo):
    """
        implementation of the Gale-Shapley algorithm to find stable matching between two groups

        :param groupOne: preference lists of members of the first group
        :param groupTwo: preference lists of members of the second group
    """
    # list to store the matching
    matching = [None] * len(groupOne)                           # --> Complexity: O(n)
    # while any member of first group is unmatched
    while None in matching:                                     # --> Complexity: O(n)
        ''' choosing the asker that hasn't been matched and 
        its highest preference that hasn't been asked '''
        currAsker = matching.index(None)                        # --> Complexity: O(n)
        highestPref = groupOne[currAsker][0]

        # if asker's current highest preference is already matched with someone else
        if highestPref in matching:                             # --> Complexity: O(n)
            ''' check the priority of asker on the preference's 
             priority list and choosing the higher priority '''
            if groupTwo[highestPref].index(currAsker) < \
                    groupTwo[highestPref].index(matching.index(highestPref)):   # --> Complexity: O(n + n + n) = O(3n)
                matching[matching.index(highestPref)] = None                    # --> Complexity: O(n)
                matching[currAsker] = highestPref
        # if asker's highest preference is also unmatched
        else:
            matching[currAsker] = highestPref

        ''' remove the current highest preference from the preference list to denote that
        the asker has already asked that preference '''
        groupOne[currAsker].pop(0)                              # --> Complexity: O(n)
    return matching

if __name__ == '__main__':
    n = int(input())

    # reading the preference lists of groupOne's members
    groupOne = []
    for i in range(n):
        inpList = input().strip().split(" ")
        prefList = [int(i) for i in inpList]
        groupOne.append(prefList)

    # reading the preference lists of groupTwo's members
    groupTwo = []
    for i in range(n):
        inpList = input().strip().split(" ")
        prefList = [int(i) for i in inpList]
        groupTwo.append(prefList)

    # obtaining two matchings by switching the groups in Gale-Shapley algorithm
    matchOne = stableMatch(deepcopy(groupOne), deepcopy(groupTwo))
    matchTwo = stableMatch(deepcopy(groupTwo), deepcopy(groupOne))

    # checking if both the matchings are same or not and printing the output
    match = True
    for i in range(n):
        if matchOne[i] != matchTwo.index(i):
            match = False
            break
    print("YES" if not match else "NO")
