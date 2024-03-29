# -*- coding: utf-8 -*-
# Advent of code working directories creator
# IMPORTANT Remember to edit the USER_SESSION_ID & author values with yours
# uses requests module. If not present use pip install requests
# Author = Alexe Simon
# Date = 06/12/2018
# https://github.com/AlexeSimon/adventofcode

# USER SPECIFIC PARAMETERS
# Folders will be created here. If you want to make a parent folder, change this to ex "./adventofcode/"
# Imports
try:
    from dotenv import dotenv_values
except ImportError:
    exit('ERROR! You need to install "python-dotenv" module: pip install python-dotenv')
try:
    import requests
except ImportError:
    exit('ERROR! You need to install "requests" module: pip install requests')
import os

# import datetime


# config = {'USER': 'foo', 'EMAIL': 'foo@example.org'}
config = dotenv_values('.env')

base_pos = './'
# Get your session by inspecting the session cookie content in your web browser while connected to adventofcode and paste it here as plain text in between the '. Leave at is to not download inputs.
USER_SESSION_ID = config['USER_SESSION_ID']

# Name automatically put in the code templates.
AUTHOR = config['AUTHOR']

# Set to false to not download statements. Note that only part one is downloaded (since you need to complete it to access part two)
DOWNLOAD_STATEMENTS = True

# Set to false to not download inputs. Note that if the USER_SESSION_ID is wrong or left empty, inputs will not be downloaded.
DOWNLOAD_INPUTS = True

# Set to false to not make code templates. Note that even if OVERWRITE is set to True, it will never overwrite codes.
MAKE_CODE_TEMPLATE = True

# Set to false to not create a direct url link in the folder.
MAKE_URL = True

# If you really need to download the whole thing again, set this to true. As the creator said, AoC is fragile; please be gentle. Statements and Inputs do not change. This will not overwrite codes.
OVERWRITE = config['OVERWRITE']


# Code template
CODE_TEMPLATE_TEXT = """


def read_file() -> str:
    with open(
        file=(__file__.rstrip('code.py') + 'input.txt'), mode='r', encoding='utf-8'
    ) as input_file:
        input_data = input_file.read()
    return input_data


def parse_input(input_data: str) -> list:
    # Parces input string to list of integers
    input_list = input_data.split('\\n')
    return input_list


def part_1(data: list[str]) -> int:
    pass


TEST_DATA = \"\"\"x
y
z\"\"\"


def part_2(data: list[str]) -> int:
    pass


# --- MAIN ---
if __name__ == '__main__':
    in_data = read_file()
    in_data = TEST_DATA  # comment out to use real data
    in_data = parse_input(in_data)
    print(f'Part One : {part_1(in_data)}')
    print(f'Part Two : {part_2(in_data)}')
"""

# DATE SPECIFIC PARAMETERS
# Date text automatically put in the code templates.
date = config['DATE']
# You can go as early as 2015.
starting_advent_of_code_year = int(config['STARTING_ADVENT_OF_CODE_YEAR'])
# The setup will download all advent of code data up until that date included
last_advent_of_code_year = int(config['LAST_ADVENT_OF_CODE_YEAR'])
# If the year isn't finished, the setup will download days up until that day included for the last year
last_advent_of_code_day = int(config['LAST_ADVENT_OF_CODE_DAY'])


# Code
MAX_RECONNECT_ATTEMPT = 2
years = range(starting_advent_of_code_year, last_advent_of_code_year + 1)
days = range(1, 26)

# ex use : https://adventofcode.com/2017/day/19/input
link = 'https://adventofcode.com/'

USER_AGENT = 'adventofcode_working_directories_creator'

print(
    'Setup will download data and create working directories and files for adventofcode.'
)
if not os.path.exists(path=base_pos):
    os.mkdir(path=base_pos)
for y in years:
    print(f'Year {y}')
    if not os.path.exists(base_pos + str(y)):
        os.mkdir(base_pos + str(y))
    year_pos = base_pos + str(y)
    for d in (
        d
        for d in days
        if (y < last_advent_of_code_year or d <= last_advent_of_code_day)
    ):
        print(f'\tDay {d}')
        if not os.path.exists(path=year_pos + '/' + str(d)):
            os.mkdir(path=year_pos + '/' + str(d))
        day_pos = year_pos + '/' + str(d)
        if MAKE_CODE_TEMPLATE and not os.path.exists(path=day_pos + '/code.py'):
            code = open(file=day_pos + '/code.py', mode='w+')
            code.write(
                '# -*- coding: utf-8 -*-\n#\n'
                + f'# Advent of code: Year {y} Day {d} solution\n'
                + f'# Author = {AUTHOR}\n'
                + f'# Date = {date}'
                + CODE_TEMPLATE_TEXT
            )
            code.close()
        if (
            DOWNLOAD_INPUTS
            and (not os.path.exists(path=day_pos + '/input.txt') or OVERWRITE)
            and USER_SESSION_ID != ''
        ):
            done = False
            error_count = 0
            while not done:
                try:
                    with requests.get(
                        url=link + str(y) + '/day/' + str(d) + '/input',
                        cookies={'session': USER_SESSION_ID},
                        headers={'User-Agent': USER_AGENT},
                    ) as response:
                        if response.ok:
                            data = response.text
                            in_file = open(file=day_pos + '/input.txt', mode='w+')
                            in_file.write(data.rstrip('\n'))
                            in_file.close()
                        else:
                            print('\t\tServer response for input is not valid.')
                    done = True
                except requests.exceptions.RequestException:
                    error_count += 1
                    if error_count > MAX_RECONNECT_ATTEMPT:
                        print('\t\tGiving up.')
                        done = True
                    elif error_count == 0:
                        print(
                            '\t\tError while requesting input from server. Request probably timed out. Trying again.'
                        )
                    else:
                        print('\t\tTrying again.')
                except Exception as e:
                    print(
                        f'\t\tNon handled error while requesting input from server. {e}'
                    )
                    done = True
        if DOWNLOAD_STATEMENTS and (
            not os.path.exists(day_pos + '/statement.html') or OVERWRITE
        ):
            done = False
            error_count = 0
            while not done:
                try:
                    with requests.get(
                        url=link + str(y) + '/day/' + str(d),
                        cookies={'session': USER_SESSION_ID},
                        headers={'User-Agent': USER_AGENT},
                    ) as response:
                        if response.ok:
                            html = response.text
                            start = html.find('<article')
                            end = html.rfind('</article>') + len('</article>')
                            end_success = html.rfind('</code>') + len('</code>')
                            statement = open(day_pos + '/statement.html', 'w+')
                            statement.write(html[start : max(end, end_success)])
                            statement.close()
                        done = True
                except requests.exceptions.RequestException:
                    error_count += 1
                    if error_count > MAX_RECONNECT_ATTEMPT:
                        print(
                            '\t\tError while requesting statement from server. Request probably timed out. Giving up.'
                        )
                        done = True
                    else:
                        print(
                            '\t\tError while requesting statement from server. Request probably timed out. Trying again.'
                        )
                except Exception as e:
                    print(
                        f'\t\tNon handled error while requesting statement from server. {e}'
                    )
                    done = True
        if MAKE_URL and (not os.path.exists(path=day_pos + '/link.url') or OVERWRITE):
            url = open(day_pos + '/link.url', 'w+')
            url.write(
                '[InternetShortcut]\nURL=' + link + str(y) + '/day/' + str(d) + '\n'
            )
            url.close()
print(
    'Setup complete : adventofcode working directories and files initialized with success.'
)
