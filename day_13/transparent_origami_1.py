#!/usr/bin/env python

import numpy as np


def fold(arr, fold):
    # Horiazontal fold
    if fold[1] == 0:
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
        fold_col = fold[1]
        col_delta, col = 0, fold_col - 1
        while fold_col - col_delta >= 0 and fold_col + col_delta + 1 < arr.shape[1]:
            for row in range(len(arr)):
                arr[row, col - col_delta] += arr[row, fold_col + col_delta + 1]
            col_delta += 1

        # Strip everything to the rigth of the folded column
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

    for _fold in folds:
        arr = fold(arr, _fold)
        break

    vals, counts = np.unique(arr, return_counts=True)
    print(arr.size - counts[list(vals).index(0)])
