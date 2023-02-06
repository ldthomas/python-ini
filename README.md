# A Python INI File Parser

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

### Installation

The Python INI file parser can be installed from either
[Github](https://github.com/ldthomas/python-ini)
or
[PyPI](https://pypi.org/project/python-ini/)

A quick start guide using the GitHub installation can be found
[**here**](https://github.com/ldthomas/python-ini/blob/main/docs/quick_github.md).

A quick start guide using the PyPI installation can be found
[**here**](https://github.com/ldthomas/python-ini/blob/main/docs/quick_pip.md).

### Documentation

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
