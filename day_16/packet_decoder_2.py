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
    def __init__(self):
        self.version = None
        self.type_id = None
        self.sub_packets = []
        self.value = None

    def __str__(self, indent=0):
        output = ' ' * indent
        if self.type_id == 4:
            output += f'Value Packet: {self.value} v{self.version} t{self.type_id}\n'
        else:
            output += f'Operator Packet: {self.operator} v{self.version} t{self.type_id} ({len(self.sub_packets)} sub packets)\n'

        for packet in self.sub_packets:
            output += packet.__str__(indent=indent + 2)
        return output


class Parser:
    def __init__(self, string):
        self.string = string
        self.i = 0
        self.root_packet = self.get_next_packet()

    def get_next_packet(self):
        version = int(self.string[self.i:self.i + 3], 2)
        self.i += 3

        type_id = int(self.string[self.i:self.i + 3], 2)
        self.i += 3

        value_string = ''
        sub_packets = []

        if type_id == 4:
            while True:
                value_string += self.string[self.i + 1:self.i + 5]
                if int(self.string[self.i:self.i + 1], 2) == 0:
                    self.i += 5
                    break
                self.i += 5

        else:
            length_type_id = int(self.string[self.i], 2)
            self.i += 1

            if length_type_id == 0:
                end = self.i + 15 + int(self.string[self.i:self.i + 15], 2)
                self.i += 15
                while self.i < end:
                    packet = self.get_next_packet()
                    sub_packets.append(packet)

            else:
                count = int(self.string[self.i:self.i + 11], 2)
                self.i += 11
                for _ in range(count):
                    sub_packets.append(self.get_next_packet())

        packet = Packet()
        packet.version = version
        packet.type_id = type_id
        packet.value = int(value_string, 2) if len(value_string) else None
        packet.sub_packets = sub_packets if len(sub_packets) else []
        return packet


def process_packet(packet):
    if packet.type_id == 4:
        return packet.value

    if packet.type_id == 0:
        return sum(process_packet(child) for child in packet.sub_packets)

    if packet.type_id == 1:
        product = 1
        for child in packet.sub_packets:
            product *= process_packet(child)
        return product

    if packet.type_id == 2:
        return min(process_packet(child) for child in packet.sub_packets)

    if packet.type_id == 3:
        return max(process_packet(child) for child in packet.sub_packets)

    if packet.type_id == 5:
        return process_packet(packet.sub_packets[0]) > process_packet(packet.sub_packets[1])

    if packet.type_id == 6:
        return process_packet(packet.sub_packets[0]) < process_packet(packet.sub_packets[1])

    if packet.type_id == 7:
        return process_packet(packet.sub_packets[0]) == process_packet(packet.sub_packets[1])


if __name__ == '__main__':
    with open('input.txt') as f:
        line = f.read().strip()

    binary = ''.join(HEX_BIN[char] for char in line)
    parser = Parser(binary)
    # print(parser.root_packet)
    print(process_packet(parser.root_packet))
