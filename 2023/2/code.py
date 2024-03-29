# -*- coding: utf-8 -*-
# Advent of code Year 2023 Day 2 solution
# Author = Andrej Kurusiov
# Date = December 2023

import re


def read_file() -> str:
    with open(
        (__file__.rstrip('code.py') + 'input.txt'), 'r', encoding='utf-8'
    ) as input_file:
        input_data = input_file.read()
    return input_data


def parse_input(input_data: str) -> list:
    # Parces input string to list of integers
    input_list = input_data.split('\n')
    return input_list


def part_1(data: list[str]) -> int:
    """Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.
    What is the sum of the IDs of those games?
    ==> 2716"""

    max_balls = {'red': 12, 'green': 13, 'blue': 14}
    ids_res = []
    for i, line in enumerate(data):
        takes = re.findall(r'(\d+) (red|green|blue)', line)
        for take in takes:
            n, color = int(take[0]), take[-1]
            if n > max_balls.get(color, 0):
                break
        else:
            ids_res.append(i + 1)
    return sum(ids_res)


TEST_DATA = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''
# Game 1: min 4 red, 2 green, and 6 blue cubes --> power=4*2*6 => 48
# Game 2: min 1 red, 3 green, and 4 blue cubes --> 12
# Game 3-5: 1560, 630, 36
# Answer: 48+12+1560+630+36 = 2286.


def part_2(data: list[str]) -> int:
    """For each game, find the minimum set of cubes that must have been present.
    What is the sum of the power of these sets?"""
    # from functools import reduce
    from math import prod

    ans = 0
    for line in data:
        min_balls = {'red': 0, 'green': 0, 'blue': 0}
        takes = re.findall(r'(\d+) (red|green|blue)', line)
        for take in takes:
            n, color = int(take[0]), take[-1]
            if n > min_balls.get(color, 0):
                min_balls[color] = n
        # ans += reduce(lambda x, y: x * y, min_balls.values())
        ans += prod(min_balls.values())
    return ans


# --- MAIN ---
if __name__ == '__main__':
    in_data = read_file()
    # in_data = TEST_DATA  # comment out to use real data
    in_data = parse_input(in_data)
    print('Part One : ' + str(part_1(in_data)))
    print('Part Two : ' + str(part_2(in_data)))
