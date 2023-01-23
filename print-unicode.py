#!/usr/bin/python3

import os
import sys
import codecs

import urllib.request
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.error import ContentTooShortError

from collections import namedtuple
from typing import List
import argparse


Range = namedtuple('Range', ['begin', 'end', 'description', 'order'])


#########
def process_arguments():
    parser = argparse.ArgumentParser(description='A script to print characters to and from unicode.')
    parser.add_argument('-l', '--list', action='store_true', help='Print list of Unicode blocks"')
    parser.add_argument('-b', '--block', type=int, help='Print all characters inside a specific Unicode BLOCK')
    parser.add_argument('-u', '--unicode', type=str, help='Print UNICODE character in decimal, UTF-32BE, UTF-8 and UTF-16LE')
    parser.add_argument('-d', '--decimal', type=int, help='Print DECIMAL character in UTF-32BE, UTF-8 and UTF-16LE')
    parser.add_argument('CHARACTERS', nargs='*', help='Print the input CHARACTERS as decimal, UTF-32BE, UTF-8 and UTF-16LE')
    return parser.parse_args()


#########
def download_file(filename, url):
    if not os.path.exists(filename):
        print(f"Downloading file from:", url)
        try:
            urllib.request.urlretrieve(url, filename)
        except URLError as e:
            print(f'Error: {e.reason}')
        except HTTPError as e:
            print(f'Error: {e.code} {e.reason}')
        except ContentTooShortError as e:
            print(f'Error: {e}')


#########
def split_line(line):
    parts = line.split("; ")
    values = parts[0].split("..")
    begin = int(values[0],16)
    if (begin < 32):
        begin = 32
    end = int(values[1],16)
    description = parts[1]
    return begin, end, description


#########
def read_file(filename):
    ranges = []
    order = 0
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            else:
                order += 1
            begin, end, description = split_line(line)
            ranges.append(Range(begin, end, description, order))
    return ranges


#########
def read_unicode_blocks_file():
    filename="Blocks.txt"
    url="https://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt"
    download_file(filename, url)
    ranges = read_file(filename)
    return ranges


#########
def print_unicode_blocks(ranges):
    for i, r in enumerate(ranges):
        print(f"{i+1}. [{hex(r.begin)}..{hex(r.end)}] {r.description}")


#########
def print_encodings(ranges, decimal):
    char=chr(decimal)
    utf8_hex = codecs.encode(char, 'utf-8').hex()
    utf16le_hex = codecs.encode(char, 'utf-16le').hex()
    utf32be_hex = codecs.encode(char, 'utf-32be').hex()
    order, description = get_range_description(ranges, decimal)
    str_order=str(order).zfill(3)

    column_width = 9
    print(f'{decimal}'.rjust(column_width),
          f'{utf32be_hex}'.rjust(column_width),
          f'{utf8_hex}'.rjust(column_width),
          f'{utf16le_hex}'.rjust(column_width),
          f'{char}'.rjust(4),
          f'\t   {str_order}'.rjust(7),
          f'    {description}')

    #print(f'd:{decimal}\tUTF-32BE:{utf32be_hex}\tUTF-8:{utf8_hex}\tUTF-16LE:{utf16le_hex}\t Char: {char}\t{order}. {description}')

def print_header():
    column_width = 9
    print('Decimal'.rjust(column_width),
          'UTF-32BE'.rjust(column_width),
          'UTF8  '.rjust(column_width),
          'UTF-16LE'.rjust(column_width),
          'Char'.rjust(column_width-3),
          'Block'.rjust(column_width-1),
          '   Block description')

def print_seperator():
    column_width = 9
    print('────────'.rjust(column_width),
          '────────'.rjust(column_width),
          '────────'.rjust(column_width),
          '────────'.rjust(column_width),
          '──────'.rjust(column_width-2),
          '───────'.rjust(column_width-1),
          ' ────────────────────────')

def print_header_top():
    print("")
    print_header()
    print_seperator()

def print_header_bottom():
    print_seperator()
    print_header()



#########
def print_unicode_block_n(ranges, block):
    if ((block < 1) or (block > 327)):
        print(f"{block} out of range")
        exit(-1)

    print_header_top()
    for i in range(ranges[block-1].begin, ranges[block-1].end+1):
        print_encodings(ranges, i)
    print_header_bottom()

    print(f"\n{block}. [{hex(ranges[block-1].begin)}..{hex(ranges[block-1].end)}] {ranges[block-1].description}\n")


#########
def print_from_unicode(uni):
    i=int(uni,16)
    print_encodings(ranges, i)


#########
def print_from_decimal(i):
    print_encodings(ranges, i)


#########
def print_from_list_of_chars(list_of_chars):
    for char in list_of_chars:
        decimal = ord(char)
        print_encodings(ranges, decimal)


#########
def get_range_description(ranges: List[Range], D: int) -> None:
    for r in ranges:
        if r.begin <= D <= r.end:
            return r.order, r.description
    return "-1", "Not found in any block range"



##################
# Main
##################

args = process_arguments()
ranges = read_unicode_blocks_file()

if args.list:
    print_unicode_blocks(ranges)

if args.block:
    print_unicode_block_n(ranges, args.block)

if args.unicode or args.decimal or args.CHARACTERS:
    print_header_top()

if args.unicode:
    print_from_unicode(args.unicode)

if args.decimal:
    print_from_decimal(args.decimal)

if args.CHARACTERS:
    print_from_list_of_chars(args.CHARACTERS)

