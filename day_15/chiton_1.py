#!/usr/bin/env python

import numpy as np
from queue import PriorityQueue


class Graph:
    def __init__(self, num_verticies):
        self.num_verticies = num_verticies
        self.edges = [[-1 for i in range(num_verticies)] for j in range(num_verticies)]
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight


def dijkstra(graph, start_vertex):
    costs = {i: np.inf for i in range(graph.num_verticies)}
    costs[start_vertex] = 0

    queue = PriorityQueue()
    queue.put((0, start_vertex))

    while not queue.empty():
        (dist, current_vertex) = queue.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.num_verticies):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = costs[neighbor]
                    new_cost = costs[current_vertex] + distance
                    if new_cost < old_cost:
                        queue.put((new_cost, neighbor))
                        costs[neighbor] = new_cost
    return costs


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()

    arr = np.zeros((len(lines), len(lines[0])), dtype=int)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            arr[row, col] = int(char)

    index_arr = np.zeros((len(arr), len(arr[0])), dtype=int)
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            index_arr[row, col] = row * len(arr) + col

    graph = Graph(len(arr) * len(arr[0]))
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            if row >= 1:
                graph.add_edge(index_arr[row, col], index_arr[row - 1, col], arr[row - 1, col])
            if row + 1 < len(arr):
                graph.add_edge(index_arr[row, col], index_arr[row + 1, col], arr[row + 1, col])
            if col >= 1:
                graph.add_edge(index_arr[row, col], index_arr[row, col - 1], arr[row, col - 1])
            if col + 1 < len(arr[0]):
                graph.add_edge(index_arr[row, col], index_arr[row, col + 1], arr[row, col + 1])

    print(dijkstra(graph, 0)[index_arr[len(arr) - 1, len(arr[0]) - 1]])
