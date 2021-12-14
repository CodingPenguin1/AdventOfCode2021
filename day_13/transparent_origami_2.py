#!/usr/bin/env python

import numpy as np


def print_arr(arr, fold_row=None, fold_col=None, blank_char='.'):
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            if arr[row, col]:
                print('#', end='')
            elif row == fold_row:
                print('-', end='')
            elif col == fold_col:
                print('|', end='')
            else:
                print(blank_char, end='')
        print()
    print()


def fold(arr, fold):
    # Horiazontal fold
    if fold[1] == 0:
        # print(f'Folding on y={fold[0]}')
        # print_arr(arr, fold_row=fold[0])
        fold_row = fold[0]
        row_delta, row = 0, fold_row - 1
        while fold_row - row_delta >= 0 and fold_row + row_delta + 1 < arr.shape[0]:
            for col in range(len(arr[0])):
                arr[row - row_delta, col] += arr[fold_row + row_delta + 1, col]
            row_delta += 1
        # Strip everything below the folded row
        arr = arr[:fold_row]

    # Vertical fold
    else:
        # print(f'Folding on x={fold[1]}')
        # print_arr(arr, fold_col=fold[1])
        fold_col = fold[1]
        col_delta, col = 0, fold_col - 1
        while fold_col - col_delta >= 0 and fold_col + col_delta + 1 < arr.shape[1]:
            for row in range(len(arr)):
                arr[row, col - col_delta] += arr[row, fold_col + col_delta + 1]
            col_delta += 1

        # Strip everything below the folded row
        arr = arr[:, :fold_col]

    return arr


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()

    # Get max value of lines
    max_x, max_y = 0, 0
    for line in lines:
        if line == '\n':
            break
        n0, n1 = line.split(',')
        if int(n0) > max_x:
            max_x = int(n0)
        if int(n1) > max_y:
            max_y = int(n1)

    arr = np.zeros((max_y + 1, max_x + 1), dtype=int)
    folds = []
    for line in lines:
        # Record fold instructions
        if line.startswith('fold along '):
            instruction = line.split(' ')[-1]
            axis = instruction[0]
            value = int(instruction[2:])
            if axis == 'x':
                folds.append((0, value))
            else:
                folds.append((value, 0))

        # Set initial points
        elif line != '\n':
            coords = (int(line.split(',')[1]), int(line.split(',')[0]))
            arr[coords] = 1

    # print_arr(arr)
    # print(arr.shape)
    for _fold in folds:
        # print(_fold)
        arr = fold(arr, _fold)
        # print_arr(arr)
    print_arr(arr, blank_char=' ')
