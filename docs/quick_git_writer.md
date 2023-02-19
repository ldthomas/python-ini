## A Quick Start INI Writer Example from the GitHub Installation

### The Project Structure

Throughout this example we will assume the project structure:

```bash
|my_project_folder
|---|python-ini-main.zip
    |my_project
    |---__init__.py
    |---write.py
```

All commands will be executed from the `my_project_folder` directory.
The content of the files will be presented and explained as we go.

### Installation

Make sure the PyPI version of `python-ini` is not installed.
Otherwise it will override the local GitHub version. However, `apg-py` must be installed.

```bash
pip uninstall python-ini
pip install apg-py
```

Install the GitHub version of `python-ini`.

```bash
unzip python-ini-main.zip
cp -r python-ini-main/python_ini .
```

### Create, Print and Write an INI file

The code , `write.py` could look somthing like this.

```python
import sys
import os
sys.path.append(os.getcwd()) # required to find python_ini
from python_ini.ini_file import IniFile
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

# print the formatted INI file
print(w.to_string())

# write the formatted INI file, parse it and remove it
fname = 'output.ini'
w.write(fname)
ini = IniFile('m')
ini.parse(fname)
if(ini.errors):
    print('parsing errors in file ' + fname)
    print(ini.display_errors())
else:
    print('INI file ' + fname + ' parsed without errors')
os.remove(fname)
print('INI file ' + fname + ' removed')
```

Execute the command:

```bash
python3 my_project/write.py
```

You should see the results:

```

# global keys
Unicode: 'a\U0010ffffb'       # max Unicode character
flags: TRUE, OFF, void        # all "booleans"

# first section
[__SECTION__]                 # this is a section
section_key: 1, 2, 3
long-value: 'abc\xffdef\ue000ghi\U0010ffffjkl'
                              # hex and Unicode string characters

INI file output.ini parsed without errors
INI file output.ini removed
```
