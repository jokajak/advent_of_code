"""AoC 16, 2021"""

# Standard library imports
import math
from dataclasses import dataclass
from aocd import data as input_data, submit


def ensure_binary(hex_str: str) -> str:
    # don't convert binary
    if all([c in ("0", "1") for c in hex_str]):
        return hex_str
    ret = ""
    for entry in hex_str:
        ret = f"{ret}{int(entry, 16):04b}"
    return ret


@dataclass
class Packet:
    """BITS Packet class.

    Every packet begins with a standard header: the first three bits encode the packet version, and the next three bits
    encode the packet type ID. These two values are numbers; all numbers encoded in any packet are represented as binary
    with the most significant bit first. For example, a version encoded as the binary sequence 100 represents the number
    4.
    """

    version: int
    type_id: int
    bits: str
    extra_bits: str

    def __init__(self, bits: str) -> None:
        # Convert hex string to binary string
        bits = ensure_binary(bits)
        if len(bits) <= 6:
            raise ValueError("Not enough bits")
        self.bits = bits
        self.sub_packets = []
        # save version as an int
        self.version = int(bits[0:3], 2)
        # save type_id as an int
        self.type_id = int(bits[3:6], 2)
        self.extra_bits = ""

    @classmethod
    def get_type_id(cls, bits: str) -> int:
        """Get the type_id of a bits packet"""
        bits = ensure_binary(bits)
        type_id = int(bits[3:6], 2)
        return type_id

    @classmethod
    def get_type(cls, bits: str):
        """Get packet type for new objects.

        Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some
        calculation on one or more sub-packets contained within.
        """
        type_id = cls.get_type_id(bits)
        if type_id == 4:
            return LiteralValuePacket
        else:
            return OperatorPacket

    @property
    def as_hex(self) -> str:
        return f"{int(self.bits, 2):X}"


@dataclass
class LiteralValuePacket(Packet):
    value: int

    def __init__(self, bits: str) -> None:
        """LiteralValuePacket representation.

        Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number. To do
        this, the binary number is padded with leading zeroes until its length is a multiple of four bits, and then it
        is broken into groups of four bits. Each group is prefixed by a 1 bit except the last group, which is prefixed
        by a 0 bit. These groups of five bits immediately follow the packet header. For example, the hexadecimal string
        D2FE28 becomes:
        """
        super().__init__(bits)
        value = self.bits[6:]
        value_bits = []
        for i in range(0, len(value), 5):
            value_bits.extend(value[i + 1 : i + 5])
            # last value
            if int(value[i]) == 0:
                last_bit = i + 5
                break
        self.value = int("".join(value_bits), 2)
        self.bits = self.bits[:last_bit]
        self.extra_bits = value[last_bit:]

    @property
    def get_version_ids(self):
        return [self.version]


@dataclass
class OperatorPacket(Packet):
    length_type_id: int
    sub_packets: list

    def __init__(self, bits: str) -> None:
        """Model an operator packet.

        An operator packet contains one or more packets. To indicate which subsequent binary data represents its
        sub-packets, an operator packet can use one of two modes indicated by the bit immediately after the packet
        header; this is called the length type ID:

        * If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the
          sub-packets contained by this packet.
        * If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets
          immediately contained by this packet.

        """
        super().__init__(bits)
        self.length_type_id = int(self.bits[6], 2)
        if self.length_type_id == 0:
            # total length in bits of the sub-packets
            sub_packet_bits = int(self.bits[7 : 7 + 15], 2)
            sub_packets = self.bits[(7 + 15) : (7 + 15 + sub_packet_bits)]
            new_packet = decode_packet(sub_packets)
            while new_packet:
                self.sub_packets.append(new_packet)
                # convert bits to hex for decode_packet
                new_packet = decode_packet(new_packet.extra_bits)
                # remove extra bits from the previous packet
            self.extra_bits = self.bits[(7 + 15 + sub_packet_bits):]

        elif self.length_type_id == 1:
            # total number of sub-packets
            sub_packet_count = int(self.bits[7 : 7 + 11], 2)
            sub_packets = self.bits[7 + 11 :]
            packet = decode_packet(sub_packets)
            while packet and len(self.sub_packets) < sub_packet_count:
                self.sub_packets.append(packet)
                packet = decode_packet(packet.extra_bits)
            assert len(self.sub_packets) == sub_packet_count
            self.extra_bits = self.sub_packets[-1].extra_bits

    @property
    def get_version_ids(self):
        version_ids = [self.version]
        for packet in self.sub_packets:
            version_ids.extend(packet.get_version_ids)
        return version_ids

    @property
    def value(self) -> int:
        """Calculate value of contained packets.

        Now that you have the structure of your transmission decoded, you can calculate the value of the expression it represents.

        * Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they
          only have a single sub-packet, their value is the value of the sub-packet.
        * Packets with type ID 1 are product packets - their value is the result of multiplying together the values of
          their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        * Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        * Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        * Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is
          greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have
          exactly two sub-packets.
        * Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less
          than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two
          sub-packets.
        * Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal
          to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two
          sub-packets.
        """

        def more_than(sub_packets):
            if sub_packets[0] > sub_packets[1]:
                return 1
            return 0

        def less_than(sub_packets):
            if sub_packets[0] < sub_packets[1]:
                return 1
            return 0

        def equal(sub_packets):
            if sub_packets[0] == sub_packets[1]:
                return 1
            return 0

        functions = {
            0: sum,
            1: math.prod,
            2: min,
            3: max,
            5: more_than,
            6: less_than,
            7: equal
        }

        return functions[self.type_id]([packet.value for packet in self.sub_packets])


def decode_packet(packet: str) -> Packet:
    """Decode a packet.

    Every packet begins with a standard header: the first three bits encode the packet version, and the next three bits
    encode the packet type ID. These two values are numbers; all numbers encoded in any packet are represented as binary
    with the most significant bit first. For example, a version encoded as the binary sequence 100 represents the number
    4.
    """
    try:
        packet_type = Packet.get_type(packet)
        return packet_type(packet)
    except ValueError:
        return None


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def part1(data):
    """Solve part 1.

    Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version
    numbers in all packets?
    """
    packet = decode_packet(data)
    return sum(packet.get_version_ids)


def part2(data):
    """Solve part 2.

    Now that you have the structure of your transmission decoded, you can calculate the value of the expression it represents.

    Literal values (type ID 4) represent a single number as described above. The remaining type IDs are more interesting:

    * Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only
      have a single sub-packet, their value is the value of the sub-packet.
    * Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their
      sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    * Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    * Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    * Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater
      than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two
      sub-packets.
    * Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than
      the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two
      sub-packets.
    * Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to
      the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two
      sub-packets.
    """
    packet = decode_packet(data)
    return packet.value


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    answer_a, answer_b = solve(puzzle_input=input_data)
    if answer_a:
        submit(answer_a, part="a")
    if answer_b:
        submit(answer_b, part="b")
