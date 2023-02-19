''' @file python_ini/ini_writer.py
@brief The IniWriter class for creating and writing an INI file.

The writer is configurable to specify optional delimiters, boolean values
and tab space for inline comments.
'''


class IniWriter:

    def __init__(self):
        '''Ini file writer constructor.
        Note that configurable values are set to defaults.
            - True = 'true'
            - False = 'false'
            - None = 'none'
            - ; for comment delimiter
            - = for key/value delimiter
            - , for value list delimiter
            - column 40 for tab to inline comments
        '''

        self.__SECTION = 0
        self.__KEY = 1
        self.__COMMENT = 2
        self.__TRUE = 'true'
        self.__FALSE = 'false'
        self.__NONE = 'none'
        self.__COMMENT_DELIM_SEMI = '; '
        self.__COMMENT_DELIM_HASH = '# '
        self.__COMMENT_TAB = 40
        self.__LINE_END = '\n'
        self.__KEY_DELIM_EQUALS = ' = '
        self.__KEY_DELIM_COLON = ': '
        self.__KEY_DELIM_SPACE = ' '
        self.__VALUE_DELIM_COMMA = ', '
        self.__VALUE_DELIM_SPACE = ' '
        self.__NAME_CHARS = [33, 36, 37, 38, 40, 41, 42, 43, 45,
                             46, 60, 62, 63, 64, 94, 95, 123, 124, 125, 126]
        self.clear()

    def clear(self):
        '''Initialize or reset the writer to its constructor defaults.'''
        self.errors = []
        self.__lines = []
        self.__comment_delim = self.__COMMENT_DELIM_SEMI
        self.__key_delim = self.__KEY_DELIM_EQUALS
        self.__value_delim = self.__VALUE_DELIM_COMMA
        self.__comment_tab = self.__COMMENT_TAB
        self.__true = self.__TRUE
        self.__false = self.__FALSE
        self.__none = self.__NONE

    def __validate_name(self, name):
        if(not isinstance(name, str)):
            return False
        for s in name:
            c = ord(s)
            if(c >= 48 and c <= 57):
                continue
            if(c >= 65 and c <= 90):
                continue
            if(c >= 97 and c <= 122):
                continue
            if(c in self.__NAME_CHARS):
                continue

            # invalid character in name
            return False
        return True

    def __normalize_comment(self, comment):
        if(comment is None):
            return None
        if(not isinstance(comment, str)):
            raise Exception(
                'IniWriter: invalid comment, must be string of ASCII characters 32-126', comment)
        elif(comment == '' or comment.isspace()):
            return ''
        for s in comment:
            c = ord(s)
            if(c >= 32 and c <= 126):
                continue
            raise Exception(
                'IniWriter: invalid character in comment - char code(' + str(c) + ')')
        return comment

    def __normalize_string(self, string):
        v = ''
        for s in string:
            c = ord(s)
            if(c >= 32 and c <= 126):
                v += s
            elif(c == 9):
                v += '\\t'
            elif(c == 10):
                v += '\\n'
            elif(c == 13):
                v += '\\r'
            elif(c == 39):
                v += "\\'"
            elif(c <= 0xff):
                h = str(hex(c))
                h = h[2:]
                if(len(h) == 1):
                    h = '0' + h
                v += '\\x' + h
            elif(c < 0xd800 or (c >= 0xe000 and c <= 0xffff)):
                h = str(hex(c))
                h = h[2:]
                while(len(h) < 4):
                    h = '0' + h
                v += '\\u' + h
            elif(c >= 0xd800 and c < 0xe000):
                raise Exception(
                    'IniWriter: string has Unicode surrogate value', string)
            elif(c <= 0x10ffff):
                h = str(hex(c))
                h = h[2:]
                while(len(h) < 8):
                    h = '0' + h
                v += '\\U' + h
            else:
                # Note: will probably never get here
                raise Exception(
                    'IniWriter: string has Unicode value out of range (>0x10FFFF)', string)
        return "'" + v + "'"

    def booleans(self, true=False, false=False, none=False):
        '''Sets the values to specify for boolean (and null) values.
        @param true If specified must be one of 'true', 'yes' or 'on', all case insensitive.
        @param false If specified must be one of 'false', 'no' or 'off', all case insensitive.
        @param none If specified must be one of 'none', 'null' or 'void', all case insensitive.
        @return Raises Exception on any parameter error.
        '''
        if(true):
            l = true.lower()
            if(l == 'true' or l == 'yes' or l == 'on'):
                self.__true = true
            else:
                raise Exception(
                    'IniWriter.booleans(): true argument must be one of "true", "yes" or "on", case insensitive',
                    true)
        if(false):
            l = false.lower()
            if(l == 'false' or l == 'no' or l == 'off'):
                self.__false = false
            else:
                raise Exception(
                    'IniWriter.booleans(): false argument must be one of "false", "no" or "off", case insensitive',
                    false)
        if(none):
            l = none.lower()
            if(l == 'none' or l == 'null' or l == 'void'):
                self.__none = none
            else:
                raise Exception(
                    'IniWriter.booleans(): none argument must be one of "none", "null" or "void", case insensitive',
                    none)

    def comment_tab(self, tab=None):
        '''Sets the column value for the tab to inline comments.
        @param tab The column value to begin inline comments.
        Must be an integer tab >= 0.
        @return Raises Exception on invalid tab value.
        '''
        if(tab is None):
            self.__comment_tab = self.__COMMENT_TAB
        elif(isinstance(tab, int) and (tab >= 0)):
            self.__comment_tab = tab
        else:
            raise Exception(
                'IniWriter.comment_tab(): argument must be positive integer', tab)

    def delimiters(self, comment=False, key=False, value=False):
        '''Sets the delimeter values.
        @param comment The comment delimiter. Must be semicolon(";") or hash("#").
        @param key The key/value delimiter. Must be equals("="), colon(":") or space.
        @param value The delimiter between multiple key values. Must be comma(",") or space.
        @return Raises Exception on invalid argument values.
        '''
        if(comment):
            if(comment == ';'):
                self.__comment_delim = self.__COMMENT_DELIM_SEMI
            elif(comment == '#'):
                self.__comment_delim = self.__COMMENT_DELIM_HASH
            else:
                raise Exception(
                    'IniWriter.comment_delimiters(): comment argument must be semicolon(":") or hash("#")', comment)
        if(key):
            if(key == '='):
                self.__key_delim = self.__KEY_DELIM_EQUALS
            elif(key == ':'):
                self.__key_delim = self.__KEY_DELIM_COLON
            elif(key.isspace()):
                self.__key_delim = self.__KEY_DELIM_SPACE
            else:
                raise Exception(
                    'IniWriter.key_delimiters(): key argument must be equals(=), comma(,) or space', key)
        if(value):
            if(value == ','):
                self.__value_delim = self.__VALUE_DELIM_COMMA
            elif(value.isspace()):
                self.__value_delim = self.__VALUE_DELIM_SPACE
            else:
                raise Exception(
                    'IniWriter.value_delimiters(): value argument must be comma(,) or space', value)

    def section(self, name, comment=None):
        '''Add a section line to the INI file.
        @param name The section name. Must be one or more characters from the set
            - a-zA-Z0-9!$%()*+-.<>?@^_{|}~
        @param comment An inline comment to add to the section name line.
        @returns Raises Exception on invalid name or comment.
        '''
        self.__validate_name(name)
        self.__lines.append(
            [self.__SECTION, name, self.__normalize_comment(comment)])

    def key(self, name, varg, comment=None):
        '''Add a key/value line to the INI file.
        @param name The key name. Must be one or more characters from the set
            - a-zA-Z0-9!$%()*+-.<>?@^_{|}~
        @param varg The value for the key. May be a single value or a list of values.
        Valid values are:
            - True
            - False
            - None
            - integer, positive or negative
            - floating point number, positive or negative
            - string
        @param comment An inline comment to add to the key/value line.
        @returns Raises Exception on invalid name, value or comment.
        '''
        self.__validate_name(name)
        if(isinstance(varg, list)):
            values = varg
        else:
            values = [varg]
        vlist = []
        for value in values:
            if(value is True):
                v = self.__true
            elif(value is False):
                v = self.__false
            elif(value is None):
                v = self.__none
            elif(isinstance(value, int) or isinstance(value, float)):
                v = str(value)
            elif(isinstance(value, str)):
                v = self.__normalize_string(value)
            else:
                raise Exception('IniWriter.key(): invalid value', value)
            vlist.append(v)
        self.__lines.append(
            [self.__KEY, name, vlist, self.__normalize_comment(comment)])

    def comment(self, comment=None):
        '''Add a comment line to the INI file.
        @param comment A comment string. Valid comments are:
            - None (default) adds a blank line
            - ' ' empty or all white space string adds a blank line
            - string of printing ASCII characters only, char codes 32-126
        @returns Raises Exception on invalid ncomment.
        '''
        self.__lines.append(
            [self.__COMMENT, self.__normalize_comment(comment)])

    def to_string(self):
        '''Convert all lines added with the section(), key() and comment() functions
        to a valid, formatted INI file.
        @returns The formatted INI file as a string.
        '''

        def indent(n):
            out = ''
            while(n):
                out += ' '
                n -= 1
            return out

        def add_comment(out, comment):
            lout = len(out)
            if(not comment):
                add = self.__LINE_END
            elif(lout >= self.__comment_tab):
                add = self.__LINE_END
                add += indent(self.__comment_tab)
                add += self.__comment_delim + comment
                add += self.__LINE_END
            else:
                add = indent(self.__comment_tab - lout)
                add += self.__comment_delim + comment
                add += self.__LINE_END
            return add

        # key line      = [id, name, value, comment]
        # section line  = [id, name, comment]
        # comment line  = [id, comment]
        out = ''
        for line in self.__lines:
            if(line[0] == self.__COMMENT):
                if(line[1] == ''):
                    out += self.__LINE_END
                else:
                    if(line[1] is None):
                        out += self.__LINE_END
                    else:
                        out += self.__comment_delim + line[1] + self.__LINE_END
            elif(line[0] == self.__KEY):
                out_line = line[1] + self.__key_delim
                count = 0
                for v in line[2]:
                    if(count > 0):
                        out_line += self.__value_delim
                    out_line += v
                    count += 1
                out += out_line + add_comment(out_line, line[3])
            else:
                out_line = '[' + line[1] + ']'
                out += out_line + add_comment(out_line, line[2])
        return out

    def write(self, fname):
        '''Write the formatted INI file to a file. Calls to_string().
        @param fname The file name to write the INI file to.
        @return Raises exceptions on file open or write errors.
        '''
        with open(fname, 'w') as fd:
            fd.write(self.to_string())
