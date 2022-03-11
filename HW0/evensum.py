"""
file: evensum.py
description: CSCI 665 Section 4 - Homework 0
language: python3
author: Divyank Kulshrestha, dk9924
"""

def evenSum():
    n = int(input())
    sum = 0
    for i in range(n):
        num = int(input())
        if num % 2 == 0:
            sum += num
    print(sum)

if __name__ == '__main__':
    evenSum()
