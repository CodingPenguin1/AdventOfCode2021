#!/usr/bin/env python


paths = []


class Cave:
    def __init__(self, name, big, connections_indicies):
        self.name = name
        self.big = big
        self.connections = connections_indicies

    def add_connection(self, connection_index):
        self.connections.append(connection_index)

    def __str__(self):
        output = f'{self.name} {"big" if self.big else "small"}\n'
        for i in self.connections:
            output += '  ' + caves[i].name + '\n'
        return output


def navigate(current_cave_index, visited, current_path, depth):
    global paths

    current_cave = caves[current_cave_index]

    if current_cave.name == 'end':
        current_path.append('end')
        paths.append(current_path)
        return

    # Update path with current cave
    current_path.append(current_cave.name)
    if not current_cave.big:
        visited[current_cave_index] += 1

    for i, cave in enumerate(caves):
        # Don't move back to start
        if cave.name != 'start':
            # Don't move to the cave we're already in
            if cave.name != current_cave.name:
                # If it's a small cave, make sure we haven't already visited it too many times
                if visited[i] < 1 or (not cave.big and max(visited) < 2):
                    # If cave is connected to current cave
                    if current_cave_index in cave.connections:
                        # Move to the cave
                        navigate(i, visited.copy(), current_path.copy(), depth + 1)
    return


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()

    # Load in caves
    caves = []
    for line in lines:
        cave_1, cave_2 = line.split('-')
        if cave_1 not in [cave.name for cave in caves]:
            caves.append(Cave(cave_1, cave_1.isupper(), []))
            cave_1_index = len(caves) - 1
        else:
            for i, cave in enumerate(caves):
                if cave.name == cave_1:
                    cave_1_index = i

        if cave_2 not in [cave.name for cave in caves]:
            caves.append(Cave(cave_2, cave_2.isupper(), []))
            cave_2_index = len(caves) - 1
        else:
            for i, cave in enumerate(caves):
                if cave.name == cave_2:
                    cave_2_index = i

        caves[cave_1_index].add_connection(cave_2_index)
        caves[cave_2_index].add_connection(cave_1_index)

    # Navigate through caves
    start_index = 0
    for i, cave in enumerate(caves):
        if cave.name == 'start':
            start_index = i
            break
    navigate(start_index, [0] * len(caves), [], 0)
    print(len(paths))
