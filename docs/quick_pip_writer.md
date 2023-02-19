## A Quick Start INI Writer Example from the PyPI Installation

### The Project Structure

Throughout this example we will assume the project structure:

```bash
|my_project_folder
    |my_project
    |---__init__.py
    |---write.py
```

All commands will be executed from the `my_project_folder` directory.
The content of the files will be presented and explained as we go.

### Installation

```bash
pip install python-ini
```

### Create, Print and Write an INI file

The code , `write.py` could look somthing like this.

```python
import os
from python_ini.ini_writer import IniWriter
from python_ini.ini_file import IniFile
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
