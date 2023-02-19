# A Python INI File Parser and Writer

## The INI File Parser

This INI file parser is simple and easy to use and yet
it retains most of the stable and varying features
of this [WikiPedia article](https://en.wikipedia.org/wiki/INI_file).
The ini file syntax is very liberal

-   allows semicolon(;) and hash(#) for comment characters
-   allows equals(=), colon(:) and space for key/value delimiters
-   allows comma(,) and space as value delimiters in multi-value mode
-   allows number, boolean and string values
-   allows unquoted, single-quoted and double-quoted strings
-   allows escaped characters in strings for:
    -   special characters
    -   control characters
    -   hexadecimal values
    -   16-bit Unicode characters
    -   32-bit Unicode characters

It supports both a single-value and multi-value mode,
allowing keys to have only one or a list of multiple values.
Its chief ommission is that it does not directly support subsections.
However, since the period is a valid section name character, section names
such as [A], [A.B] and [A.B.C] are unique section names and could be used to simulate
subsections.

Implemented with a single class and five member "getter" functions, it is easy to use
with a short learning curve. For example, this simple progrm would print all values
for all sections and keys in the file INI_FILE_NAME.

```python
from python_ini.ini_file import IniFile
ini = IniFile()                                 # default is single-value mode
ini.parse(INI_FILE_NAME)
if(ini.errors):
    print('INI FILE ERRORS')
    print(ini.display_errors())                 # display any errors found in the INI file
keys = ini.get_keys()                           # get a list of all keys in the global section
for key in keys:
    values = ini.get_values(key)                # get the value for each key
    print(key, end=': ')
    print(values)
sections = ini.get_sections()                   # get a list of all section names
for section in sections:
    keys = ini.get_section_keys(section)        # get a list of all keys in each section
        for key in keys:
            values = ini.get_section_values(section, key)   # get the value for each section key
            print('[' + section + ']:' + key, end=' ')
            print(values)
```

## The INI File Writer

The writer is implemented with a simple three functions to write:

-   comment lines
-   key/value lines
-   section name lines

For overriding the default values there are three functions for setting some options:

-   delimiters
    -   comment delimiters semicolon(;) or hash(#)
    -   key/value delimiters equals(=), colon(:) or space
    -   value list delimiters comma(,) or space
-   booleans
    -   True: true, yes, on (all case insensitive)
    -   False: false, no, off (all case insensitive)
    -   None: none, null, void (all case insensitive)
-   the comment tab - key and section lines may have an optional comment
    which is tabbed on the same line. If the line is longer than the tab column
    the comment is tabbed on the following line.

The following simple program:

```python
from python_ini.ini_writer import IniWriter
w = IniWriter()

# set all configurable values
w.delimiters('#', ':', ',')
w.booleans('TRUE', 'OFF', 'void')
w.comment_tab(30)

# global keys
w.comment()
w.comment('global keys')
w.key('Unicode', 'a\U0010ffffb', 'max Unicode character')
w.key('flags', [True, False, None], 'all "booleans"')

# section keys
w.comment()
w.comment('first section')
w.section('__SECTION__', 'this is a section')
w.key('section_key', [1, 2, 3])
w.key(
    'long-value',
    ['abc\xffdef\ue000ghi\U0010ffffjkl'],
    'hex and Unicode string characters')

# print the formatted INI file
w.write('output.ini')
```

would write the following INI file to 'output.ini'.

```
# global keys
Unicode: 'a\U0010ffffb'       # max Unicode character
flags: TRUE, OFF, void        # all "booleans"

# first section
[__SECTION__]                 # this is a section
section_key: 1, 2, 3
long-value: 'abc\xffdef\ue000ghi\U0010ffffjkl'
                              # hex and Unicode string characters
```

## Installation

The Python INI file parser and writer can be installed from either
[Github](https://github.com/ldthomas/python-ini)
or
[PyPI](https://pypi.org/project/python-ini/)

Quick start guides:

-   [GitHub INI parser](https://github.com/ldthomas/python-ini/blob/main/docs/quick_github.md)
-   [GitHub INI writer](https://github.com/ldthomas/python-ini/blob/main/docs/quick_git_writer.md)
-   [PyPI INI parser](https://github.com/ldthomas/python-ini/blob/main/docs/quick_pip.md)
-   [PyPI INI writer](https://github.com/ldthomas/python-ini/blob/main/docs/quick_pip_writer.md)

## Documentation

The full documentation is in the code and in additional documentation files.
It can be generated
with [doxygen](https://www.doxygen.nl/)
from the GitHub installation. For example, using the GitHub zip download
and the Ubuntu Linux command line:

```bash
unzip python-ini-main.zip
cd python-ini-main
sudo apt install graphviz
sudo apt install doxygen
doxygen
```

The documentation home page will now be found in `html/index.html`.
Or you can view it directly from the
[APG website](https://sabnf.com/docs/python-ini/index.html)
