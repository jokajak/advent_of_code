"""Tests for AoC 16, 2021"""

# Standard library imports
import pathlib

# Third party imports
import aoc202116
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202116.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202116.parse(puzzle_input)


@pytest.mark.parametrize(
    "input_hex, binary",
    [
        ("D2FE28", "110100101111111000101000"),
        ("38006F45291200", "00111000000000000110111101000101001010010001001000000000")
    ]
)
def test_hex_to_binary(input_hex, binary):
    assert aoc202116.hex_to_binary(input_hex) == binary


@pytest.mark.parametrize(
    "transmission,expected",
    [
        ("D2FE28", 6),
        ("EE00D40C823060", 7+2+4+1),
        ("38006F45291200", 1+6+2),
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ],
)
def test_parse_example1(transmission, expected):
    """Test that input is parsed properly"""
    packet = aoc202116.decode_packet(transmission)
    assert sum(packet.get_version_ids) == expected


@pytest.mark.skip(reason="Not implemented")
def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc202116.part1(example1) == ...


@pytest.mark.parametrize(
    "transmission,expected",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_part2_example2(transmission, expected):
    """Test part 2 on example input"""
    assert aoc202116.part2(transmission) == expected
