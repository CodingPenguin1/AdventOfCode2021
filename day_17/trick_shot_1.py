#!/usr/bin/env python

from numba import njit, prange
import numpy as np


@njit(parallel=True)
def shoot(target_x, target_y, max_ys):
    for initial_vy in prange(10000):
        for initial_vx in range(2, 1000):
            x, y, vx, vy = 0, 0, initial_vx, initial_vy

            max_y = 0
            while True:
                x += vx
                y += vy
                if vx > 0:
                    vx -= 1
                elif vx < 0:
                    vx += 1
                vy -= 1

                if y > max_y:
                    max_y = y

                if x > 1000 or y < -1000:
                    break

                if target_x[0] <= x <= target_x[1] and target_y[0] <= y <= target_y[1]:
                    max_ys[initial_vy] = max_y
                    break
    return max_ys


if __name__ == '__main__':
    with open('input.txt') as f:
        line = f.read().strip()

    x, y = line[line.find('x'):].replace('x=', '').replace('y=', '').split(', ')
    target_x = [int(i) for i in x.split('..')]
    target_y = [int(i) for i in y.split('..')]

    max_ys = np.zeros(10000, dtype=int)
    max_ys = shoot(target_x, target_y, max_ys)
    print(np.max(max_ys))
