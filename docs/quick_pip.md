## A Quick Start INI File Example from the pip Installation

### The Project Structure

Throughout this example we will assume the project structure:

```bash
|my_project_folder
|---|my_project
    |---__init__.py
    |---multiple.py
    |---multiple.ini
    |---single.py
    |---single.ini
```

All commands will be executed from the `my_project_folder` directory.
The content of the files will be presented and explained as we go.

### Installation

Make sure `python-ini` (and `apg-py`, a dependency) are installed and working.

```bash
pip install python-ini
python-ini --help
apg-py --version
```

### The Parser in Single-Value Mode

The single-valued INI file, `single.ini`, could look like this (note that it intentionally contains a few errors):

```
; single value INI file with some errors
number = 100
name = Dick
bad_escaped = "bad \y escaped"
[SECTION.1]
number = 200
flag = false
bad_hex = \xfg
[SECTION.1.1]
number = 300
flag = yes
[SECTION.1.2]
number = 400
name = 'Jim Smith'
bad_value = /value
```

The code to parse it in single-value mode, `single.py` could look somthing like this.<br>

```python
from python_ini.ini_file import IniFile

# construct the IniFile object and parse the INI file
fname = 'my_project/single.ini'
ini = IniFile('s') # parse the file in single-value mode
# or simply
ini = IniFile()    # single-value mode is the default
ini.parse(fname)

# display any errors found in the INI file
if(ini.errors):
    print('INI FILE ERRORS')
    print(ini.display_errors())

# iterate over all keys and values in the anonymous section
keys = ini.get_keys() # get a list of anonymous key names
print('\nANONYMOUS KEYS AND VALUES')
for key in keys:
    values = ini.get_values(key) # get the value for each key
    print(key, end=': ')
    print(values)

# iterate over all keys and values in all sections
sections = ini.get_sections() # get a list of section names
print('\nSECTION NAMES, KEYS AND VALUES')
for section in sections:
    keys = ini.get_section_keys(section) # get a list of key names for each section
    for key in keys: # get the value for each section key
        values = ini.get_section_values(section, key)
        print('[' + section + ']:' + key, end=' ')
        print(values)
```

Execute the command:

```bash
python3 my_project/single.py
```

You should see the results of a successful parse.

```
INI FILE ERRORS
{line: 4, message: unrecognized escaped character(\c) - char code c(121)}
{line: 8, message: hexadecimal value(\xhh) has invalid hex digit - char code(103)}
{line: 15, message: bad key/value definition}

ANONYMOUS KEYS AND VALUES
number: 100
name: Dick

SECTION NAMES, KEYS AND VALUES
[SECTION.1]:number 200
[SECTION.1]:flag False
[SECTION.1.1]:number 300
[SECTION.1.1]:flag True
[SECTION.1.2]:number 400
[SECTION.1.2]:name Jim Smith
```

### The Parser in Multi-Value Mode

The multi-valued INI file, `multiple.ini`, could look like this (note that it intentionally contains a few errors):

```
; multiple value INI file with some errors
numbers = 100,  200
names = Dick, 'Jane Doe'
bad_escaped = "bad \y escaped"
[SECTION.1]
numbers = 200, 300, 400
flags = false, no, off, null
bad_hex = \xfg
[SECTION.1.1]
numbers = 300, 400
flags = true, yes, on, void
[SECTION.1.2]
numbers = 400, 500
names = 'Jim Smith', Jane
bad_separator = 100 / 200
```

The code to parse it in multi-value mode, `multiple.py` could look somthing like this.<br>

```
from pprint import pprint
from python_ini.ini_file import IniFile

# construct the IniFile object and parse the INI file
fname = 'my_project/multiple.ini'
ini = IniFile('m') # parse the file in multi-value mode
ini.parse(fname)

# display any errors found in the INI file
if(ini.errors):
    print('INI FILE ERRORS')
    print(ini.display_errors())

# get a list of all keys an iterate through the key values
keys = ini.get_keys() # get a list of anonymous key names
print('\nANONYMOUS KEYS AND VALUES')
for key in keys:
    values = ini.get_values(key) # get the value for each key
    print(key, end=': ')
    pprint(values)

# iterate over all keys and values in all sections
sections = ini.get_sections() # get a list of section names
print('\nSECTION NAMES, KEYS AND VALUES')
for section in sections:
    keys = ini.get_section_keys(section) # get a list of key names for each section
    for key in keys:
        values = ini.get_section_values(section, key) # get the value for each section key
        print('[' + section + ']:' + key, end=' ')
        pprint(values)
```

Execute the command:

```bash
python3 my_project/multiple.py
```

You should see the results of a successful parse.

```
INI FILE ERRORS
{line: 4, message: unrecognized escaped character(\c) - char code c(121)}
{line: 8, message: hexadecimal value(\xhh) has invalid hex digit - char code(103)}
{line: 15, message: bad key/value definition}

ANONYMOUS KEYS AND VALUES
numbers: [100, 200]
names: ['Dick', 'Jane Doe']

SECTION NAMES, KEYS AND VALUES
[SECTION.1]:numbers [200, 300, 400]
[SECTION.1]:flags [False, False, False, None]
[SECTION.1.1]:numbers [300, 400]
[SECTION.1.1]:flags [True, True, True, None]
[SECTION.1.2]:numbers [400, 500]
[SECTION.1.2]:names ['Jim Smith', 'Jane']
```
