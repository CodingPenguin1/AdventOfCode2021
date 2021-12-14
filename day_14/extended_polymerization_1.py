#!/usr/bin/env python

if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()

    template = lines[0].strip()
    rules = {}
    for i in range(2, len(lines)):
        pair, insert = lines[i].strip().split(' -> ')
        insert = pair[0] + insert + pair[1]
        rules[pair] = insert

    elements = {}
    for char in template:
        if char in elements:
            elements[char] += 1
        else:
            elements[char] = 1

    pairs = {}
    for i in range(len(template) - 1):
        pair = template[i:i + 2]
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1

    STEPS = 10
    for _ in range(STEPS):
        new_pairs = pairs.copy()
        for pair, count in pairs.items():
            for _ in range(count):
                insert = rules[pair]
                for new_pair in {insert[:2], insert[1:]}:
                    if new_pair in new_pairs:
                        new_pairs[new_pair] += 1
                    else:
                        new_pairs[new_pair] = 1

                new_pairs[pair] -= 1
                if insert[1] in elements:
                    elements[insert[1]] += 1
                else:
                    elements[insert[1]] = 1

        pairs = new_pairs.copy()

    print(max(elements.values()) - min(elements.values()))
