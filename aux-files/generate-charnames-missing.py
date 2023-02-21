#!/usr/bin/python3

import os
import sys
import codecs

import urllib.request
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.error import ContentTooShortError

from collections import namedtuple

import requests
from bs4 import BeautifulSoup

Range = namedtuple('Range', ['begin', 'end', 'description', 'order'])



#########
def download_file(filename):
    url = "https://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt"

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
def read_unicode_blocks_file(filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}")
        download_file(filename)
    ranges = read_file(filename)
    return ranges


#########
def get_char_name(uchar):

    baseurl = "https://unicode-explorer.com/c/"
    url = baseurl+uchar

    # Define the headers for the request
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=HEADERS)

    # Check if the response was successful
    if response.status_code == 200:
        content = response.content

        # Parse the page content with Beautiful Soup
        soup = BeautifulSoup(content, 'lxml')

        # Find the first element with the "data-name" attribute and return its value
        data_name = soup.find(attrs={'data-name': True})['data-name'].lower()
        return data_name
    else:
        print(f"Error: {response.status_code}")
        return None



##################
# Main
##################

# Blocks.txt file location
home = os.path.expanduser("~")
basedir = home + "/.local/share/"
block_filename = basedir + "Unicode-Blocks.txt"
base_char_filename = "CharNames--"

ranges = read_unicode_blocks_file(block_filename)
char_filename = base_char_filename + "-resto.txt"

with open(char_filename, "w") as file:
    for j, r in enumerate(ranges):
        i = r.end
        if i >= 0xD800 and i <= 0xDFFF:
            continue
        else:
            char=chr(i)

            utf32be_hex = codecs.encode(char, 'utf-32be').hex()

            name=get_char_name(utf32be_hex)
            line = f"{i},{name}\n"
            file.write(line)
            if j % 10 == 0:
                print(f"Processed {j}: {name}")

file.close()
