#!/usr/bin/env python

from numba import njit, prange
import numpy as np


@njit(parallel=True)
def shoot(target_x, target_y, hits):
    for initial_vy in prange(-10000, 10000):
        for initial_vx in prange(1000):
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

                if x > 10000 or y < -10000:
                    break

                if target_x[0] <= x <= target_x[1] and target_y[0] <= y <= target_y[1]:
                    hits[initial_vy + 10000][initial_vx] = 1
                    break
    return hits


if __name__ == '__main__':
    with open('input.txt') as f:
        line = f.read().strip()

    x, y = line[line.find('x'):].replace('x=', '').replace('y=', '').split(', ')
    target_x = [int(i) for i in x.split('..')]
    target_y = [int(i) for i in y.split('..')]

    hits = np.zeros((20000, 1000), dtype=int)
    hits = shoot(target_x, target_y, hits)
    values, counts = np.unique(hits, return_counts=True)
    print(counts[1])
