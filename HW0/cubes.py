"""
file: cubes.py
description: CSCI 665 Section 4 - Homework 0
language: python3
author: Divyank Kulshrestha, dk9924
"""

def cubes(num: int):
    count = 0
    while True:
        if count**3 > num:
            break
        print(count**3)
        count += 1


if __name__ == '__main__':
    cubes(int(input()))