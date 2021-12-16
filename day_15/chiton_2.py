#!/usr/bin/env python

from queue import PriorityQueue
import numpy as np
from sys import maxsize

INT_INF = maxsize


def print_arr(arr, cur_row, cur_col, visited):
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

    for row in range(len(arr)):
        for col in range(len(arr[0])):
            formatting = ''
            if (row, col) in visited:
                formatting += BOLD
            if row == cur_row and col == cur_col:
                formatting += RED
            print(f'{formatting}{arr[row, col]}{END}', end=' ')
        print()


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()

    arr = np.zeros((len(lines) * 5, len(lines[0]) * 5), dtype=int)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            arr[row, col] = int(char)

    height, width = len(lines), len(lines[0])
    for row in range(height):
        for col in range(width):
            for row_offset in range(5):
                for col_offset in range(5):
                    if row_offset != 0 or col_offset != 0:
                        val = arr[row, col] + row_offset + col_offset
                        if val >= 10:
                            val -= 9
                        arr[row + row_offset * height, col + col_offset * width] = val

    # === Dijkstra's Algorithm === #

    height, width = len(arr), len(arr[0])

    visited = np.zeros((height, width), dtype=bool)
    risks = np.zeros((height, width), dtype=int)
    queue = PriorityQueue()
    for row in range(height):
        for col in range(width):
            risks[row, col] = INT_INF
    risks[0, 0] = 0
    queue.put((0, 0, 0))

    while not queue.empty():
        risk, cur_row, cur_col = queue.get()
        visited[cur_row, cur_col] = 1

        if cur_row == height - 1 and cur_col == width - 1:
            print(risks[-1, -1])
            quit()

        for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            row, col = cur_row + delta[0], cur_col + delta[1]
            if 0 <= row < height and 0 <= col < width and not visited[row, col]:
                new_risk = risks[cur_row, cur_col] + arr[row, col]
                old_risk = risks[row, col]
                if new_risk < old_risk:
                    risks[row, col] = new_risk
                    queue.put((new_risk + 2.2 * (height - row + width - col), row, col))

    print(risks[-1, -1])
