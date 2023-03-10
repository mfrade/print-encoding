# print-encoding
A script to print characters to and from unicode.

## Install

```Shell
pip install print-encoding
```

## Usage

```Shell
print-encoding -h
usage: print-encoding [-h] [-l] [-r] [-b BLOCK] [-u UNICODE] [-d DECIMAL] [CHARACTERS ...]

A script to print characters to and from unicode.

positional arguments:
  CHARACTERS            Print the input CHARACTERS as decimal, UTF-32BE, UTF-8 and UTF-16LE

options:
  -h, --help                        show this help message and exit
  -l, --list                        Print list of Unicode blocks
  -r, --redownload                  Re-downloads the Blocks.txt file with the unicode characters ranges
  -b BLOCK, --block BLOCK           Print all characters inside a specific Unicode BLOCK
  -u UNICODE, --unicode UNICODE     Print UNICODE character in decimal, UTF-32BE, UTF-8 and UTF-16LE
  -d DECIMAL, --decimal DECIMAL     Print DECIMAL character in UTF-32BE, UTF-8 and UTF-16LE
```

## Examples

Print the different encodings of characters `€ @`:
```Shell
print-encoding € @

  Decimal  UTF-32BE    UTF8    UTF-16LE   Char    Block    Block - char description
 ────────  ────────  ────────  ────────  ──────  ───────  ──────────────────────────
     8364  000020ac    e282ac      ac20    €       075     Currency Symbols - euro sign
       64  00000040        40      4000    @       001     Basic Latin - commercial at
```


Print all the characters in unicode block number 75:
```Shell
print-encoding -b 75

  Decimal  UTF-32BE    UTF8    UTF-16LE   Char    Block    Block - char description
 ────────  ────────  ────────  ────────  ──────  ───────  ──────────────────────────
     8352  000020a0    e282a0      a020    ₠       075     Currency Symbols - euro-currency sign
     8353  000020a1    e282a1      a120    ₡       075     Currency Symbols - colon sign
     8354  000020a2    e282a2      a220    ₢       075     Currency Symbols - cruzeiro sign
(...)

75. [0x20a0..0x20cf] Currency Symbols
```

List all unicode blocks:
```Shell
print-encoding -l
1. [0x20..0x7f] Basic Latin
2. [0x80..0xff] Latin-1 Supplement
3. [0x100..0x17f] Latin Extended-A
(...)
325. [0xe0100..0xe01ef] Variation Selectors Supplement
326. [0xf0000..0xfffff] Supplementary Private Use Area-A
327. [0x100000..0x10ffff] Supplementary Private Use Area-B
```

Print character from unicode:
```Shell
print-encoding -u 1f600

  Decimal  UTF-32BE    UTF8    UTF-16LE   Char    Block    Block - char description
 ────────  ────────  ────────  ────────  ──────  ───────  ──────────────────────────
   128512  0001f600  f09f9880  3dd800de    😀      306     Emoticons - grinning face
```
