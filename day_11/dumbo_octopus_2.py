#!/usr/bin/env python

import numpy as np


def valid_index(arr, row, col):
    return 0 <= row < len(arr) and 0 <= col < len(arr[0])


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()

    arr = np.array([[int(c) for c in line] for line in lines], dtype=int)

    step = 0
    flashed = np.zeros(arr.shape, dtype=int)
    while flashed.sum() != flashed.size:
        # Increment all by 1
        for row in range(len(arr)):
            for col in range(len(arr[0])):
                arr[row, col] += 1

        # Flash (reset to 0 on the fly)
        flashed = np.zeros(arr.shape, dtype=int)
        while arr.max() > 9:
            for row in range(len(arr)):
                for col in range(len(arr[0])):
                    if arr[row, col] > 9 and not flashed[row, col]:
                        flashed[row, col] = 1
                        arr[row, col] = 0
                        if valid_index(arr, row - 1, col) and not flashed[row - 1, col]:
                            arr[row - 1, col] += 1
                        if valid_index(arr, row - 1, col - 1) and not flashed[row - 1, col - 1]:
                            arr[row - 1, col - 1] += 1
                        if valid_index(arr, row - 1, col + 1) and not flashed[row - 1, col + 1]:
                            arr[row - 1, col + 1] += 1
                        if valid_index(arr, row, col - 1) and not flashed[row, col - 1]:
                            arr[row, col - 1] += 1
                        if valid_index(arr, row, col + 1) and not flashed[row, col + 1]:
                            arr[row, col + 1] += 1
                        if valid_index(arr, row + 1, col) and not flashed[row + 1, col]:
                            arr[row + 1, col] += 1
                        if valid_index(arr, row + 1, col - 1) and not flashed[row + 1, col - 1]:
                            arr[row + 1, col - 1] += 1
                        if valid_index(arr, row + 1, col + 1) and not flashed[row + 1, col + 1]:
                            arr[row + 1, col + 1] += 1

                        row = -1
                        break
        step += 1

    print(step)
