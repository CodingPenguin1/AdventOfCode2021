#!/usr/bin/env python


HEX_BIN = {'0': '0000',
           '1': '0001',
           '2': '0010',
           '3': '0011',
           '4': '0100',
           '5': '0101',
           '6': '0110',
           '7': '0111',
           '8': '1000',
           '9': '1001',
           'A': '1010',
           'B': '1011',
           'C': '1100',
           'D': '1101',
           'E': '1110',
           'F': '1111'}


class Packet:
    def __init__(self, string):
        self.string = ''
        for char in string:
            self.string += HEX_BIN[char]
        self.version = None
        self.type_id = None
        self.sub_packets = []

        self.value = None
        self.operator = None

        self.parse()

    def parse(self):
        self.version = int(self.string[:3], 2)
        self.type_id = int(self.string[3:6], 2)

        # Value packet
        if self.type_id == 4:
            binary_number = ''
            for i in range(6, len(self.string), 5):
                binary_number += self.string[i + 1: i + 5]
                if self.string[i] == '0':
                    break
            self.value = int(binary_number, 2)

        # Operator packet
        else:
            length_type_id = int(self.string[6], 2)
            if length_type_id == 0:
                length = int(self.string[7:22], 2)
                self.parse_sub_packets(self, self.string[22:], length=length)

    def parse_sub_packets(self, string, length=None):
        pass

    def __str__(self):
        if self.type_id == 4:
            return f'Value Packet: {self.value} v{self.version}'
        else:
            return f'Operator Packet: {self.operator} v{self.version} ({len(self.sub_packets)} sub packets)'


if __name__ == '__main__':
    with open('sample_input_1.txt') as f:
        line = f.read().strip()

    line = '38006F45291200'

    packet = Packet(line)
    print(packet)
