# A Python INI File Parser and Writer

[**Introduction**](#id_introduction)<br>
[**GitHub Installation**](#id_installation)<br>
[**PyPi Installation**](#id_pypi)<br>
[**INI File Syntax**](#id_syntax)<br>
[**Parser Usage**](#id_usage)<br>
[**Writer Usage**](#id_writer)<br>
[**License**](#id_license)

### Introduction {#id_introduction}

INI or initialization files are text-based files using simple key/value pairs
in optionally named sections for organizational purposes.
`python-ini` is a simple and easy to use INI file parser and yet
it retains most of the stable and varying features
of this [WikiPedia article](https://en.wikipedia.org/wiki/INI_file).
It supports an extremely liberal INI file syntax, operates in single- or multiple-value mode
and has "getter" functions which support default values if the key or section does not exist.
Key and comment delimiters are very flexible and
section and key names can contain almost any character that is not used as a special character elsewhere.

Its chief ommission is that it does not directly support subsections.
However, since the period is a valid section name character, section names
such as [A], [A.B] and [A.B.C] are unique section names and could be used to simulate
subsections.

### GitHub Installations {#id_installation}

`python-ini` can be installed from GitHub by either cloning it or downloading the zip file.
Throughout an Ubuntu-flavored Linux OS is assumed.

#### Cloning

From the project directory execute

```bash
git clone https://github.com/ldthomas/python-ini.git
cd python-ini
python3 python_ini --help
```

#### Zip File

Download the zip file from [https://github.com/ldthomas/python-ini](https://github.com/ldthomas/python-ini)
and execute

```bash
unzip python-ini-main.zip
cd python-ini-main
python3 python_ini --help
```

#### Testing

Unit tests are in the `tests` directory. Run

```bash
python3 -m unittest discover
```

which should indicate something like 42 successful tests.

There is also a set of examples demonstrating most aspects
of using python-ini in the `examples` directory.
Each example displays a short description of the test and its output.

```bash
python3 examples/basic.py
python3 examples/all_options.py
python3 examples/defaults.py
python3 examples/multi_values.py
python3 examples/writer.py
```

See these quick start guides for using using
the GitHub installation of `python-ini` in your project.

-   [parser](docs/quick_github.md)
-   [writer](docs/quick_git_writer.md)

### PyPi Installations {#id_pypi}

The simplest way to install `python-ini` is simply

```bash
pip install python-ini
python-ini --help
```

This will install `python-ini` and the CLI stand-alone help function
but none of the tests or examples that are available from the GitHub installation.

See these quick start guides for using using
the `pip` installation of `python-ini` in your project.

-   [parser](docs/quick_pip.md)
-   [writer](docs/quick_pip_writer.md)

### INI File Syntax {#id_syntax}

##### Keys

Key names must begin at the first character on a line, are case sensitive and must be one or more characters from the set

```
a-bA-B0-9!$%()*+-.<>?@^_{|}~
```

That is, almost any character that is not used elsewhere as a special character.

Keys are "disjoint". That is, the values for a key name appearing multiple times within a section
are combined as if they had been specified all on one line.

_Note on key values:_<br>
Keys may have a single value or a list of multiple values.
In fact, values are always interpeted as a list. When the parser is in single-value mode,
a request for a key value will simply return the last value in the list.
When in multi-value mode it will return the entire list, even if it is only a single value.
For example, consider the INI file

```
num1 = 100
num2 = 200, 300
```

In single-value mode the parser will return the key values

```
num1 = 100
num2 = 300
```

In multi-value mode the parser will return the key values

```
num1 = [100]
num2 = [200, 300]
```

##### Sections

Sections are enclosed in square brackets which must begin on the first character of a line.
Sections names, like key names, are case sensitive and are formed from one or more characters
of the same set as for keys. White space is allowed between brackets and section names. For example,
these would all be valid sections.

```
[SECTION]
[  __section__ ]
[A.B.C]
```

A section ends at the beginning of another section or at the end of the file.
Sections are "disjoint". That is, if a section name appears more than once,
the keys and values are merged as if they had occurred in a single section.

##### Values

Values may be numbers, booleans or strings.

**Numbers**<br>
Numbers may be positive or negative integers or floating point.

```
integers = 1, -100, +200
float    = 1., 2.0, +.1e10, -1.0E-2
```

**Booleans**<br>
Booleans are case insensitive and may be

```
True:   true, yes, on
False:  false, no, off
None:   none, null, void
```

(OK, "None" is not exactly boolean.) Boolean values are reserved key words and must be quoted if needed as strings.

Note that a key without a value is interpreted as a "true" flag.
That is, consider the INI file

```
false_flag = no
true_flag
```

The parser will return the values

```
false_flag = False
true_flag = True
```

**Strings**<br>
Control characters, tab, line feed, carriage return, etc., are not allowed in
any of the string forms. Escaped characters must be used (see below).

_unquoted_<br>
Unquoted strings may not be any of the reserved boolean key words.
Otherwise, they may contain any characters except [space " # ' , / : ; = \\].
(Square braces not included. They simply delimit the disallowed set.)

_single-quoted_<br>
Single-quoted strings, 'single quoted', may contain any characters except [' \\].

_double-quoted_<br>
Double-quoted strings, "double quoted", may contain any characters except [" \\].

_escaped characters_<br>
Characters otherwise not allowed in any of the string forms must be escaped.
Escaped characters begin with a back slash or reverse solidus(\\).
Escaped characters and their meaning are:

| escaped     | rendered          |
| ----------- | ----------------- |
| \\\\        | \\                |
| \\"         | "                 |
| \\#         | #                 |
| \\'         | '                 |
| \\,         | ,                 |
| \\:         | :                 |
| \\;         | ;                 |
| \\=         | =                 |
| \\b         | space             |
| \\t         | tab               |
| \\n         | line feed         |
| \\r         | carriage return   |
| \\xhh       | 8-bit hexadecimal |
| \\uhhhh     | 16-bit Unicode    |
| \\Uhhhhhhhh | 32-bit Unicode    |

Notes:<br>
h = hex digit, 0-9a-fA-F<br>
16-bit Unicode, surrogate values, 0xD800 - 0xDFFF, not allowed<br>
32-bit Unicode, surrogate values, 0xD800 - 0xDFFF, and values > 0x10FFFF not allowed

##### Delimiters

**key dilimiters**<br>
Keys may be delimited from the values with equals(=), colon(:) or simply with a space.
For example, all of the following would be valid key/value definitions.

```
A=100
B = 200
C: 300
D : 400
E 500
```

**value dilimiters**<br>
Multiple values may be delimited with commas or spaces.
For example, the following INI file

```
nums = 100,200 300  ,400 500
```

would return the multi-value list

```
nums = [100, 200, 300, 400, 500]
```

##### Line Continuations

Lines may be continued with a forward slash(/) with at least one space or tab beginning the next line.
For example,

```
list = 100, 200, / # continue the list on the next line
 300, 400
```

##### Comments

Comments begin with either a hash(#) or semicolon(;) and continue to the end of the line.
For example,

```
; this is a comment
# this is another comment
num = 100           # this is an integer value
str = "big boy"     ; this is a double-quoted string value
```

### Parser Usage {#id_usage}

Implemented with a single class and five member "getter" functions, it is easy to use
with a short learning curve. For example, this simple program would print all values
for all keys in all sections from the file INI_FILE_NAME.

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

See the constructor and member functions, python_ini.ini_file.IniFile, for detailed descriptions of options and usage.

##### Error Reporting

Note that the parser is designed to report errors in the INI file syntax without halting.
That is, the parser should never fail. It should collect all syntacticly correct
section, key values and report errors for any file lines that are syntacticly incorrect.

### Writer Usage {#id_writer}

Implemented with a single class with functions to write comments, key/value pairs and sections, it is easy to use
with a short learning curve. For example, this simple program would configure all defaults and write a short INI file.

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
    'long-key',
    ['abc\xffdef\ue000ghi\U0010ffffjkl'],
    'hex and Unicode string characters')

# write the formatted INI file
w.write('output.ini)
```

The file `output.ini` would look like this:

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

See the IniWriter class, python_ini.ini_writer.IniWriter, for the details.

### License {#id_license}

2-Clause BSD License.

<pre>
Copyright &copy; 2023 Lowell D. Thomas, all rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</pre>
