''' @file python_ini/ini_writer.py
@brief The IniWriter class for creating and writing an INI file.
'''
import sys
import os
import copy
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
# from apg_py.lib import utilities as utils
# from apg_py.lib.parser import Parser
# from apg_py.lib.trace import Trace
# from apg_py.lib.ast import Ast
# import python_ini.grammar as grammar
# import python_ini.parser_callbacks as pcb
# import python_ini.ast_callbacks as acb

# Note: The SABNF syntax for the ini file parser is in grammar.abnf.
# The grammar object, grammar.py was generated with (assuming PyPI installation of apg-py)
# python3 apg-py -i python_ini/grammar.abnf


def indent(n):
    out = ''
    if(n < 0):
        n = -n
    if(n > 120):
        n = 120
    while(n):
        out += ' '
        n -= 1
    return out


class IniWriter:

    def __init__(self):
        '''Ini file writer constructor.
        '''

        self.__SECTION = 0
        self.__KEY = 1
        self.__COMMENT = 2
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
        self.errors = []
        self.__lines = []
        self.__comment_delim = self.__COMMENT_DELIM_SEMI
        self.__key_delim = self.__KEY_DELIM_EQUALS
        self.__value_delim = self.__VALUE_DELIM_COMMA
        self.__comment_tab = self.__COMMENT_TAB

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
            elif(c <= 0x10ffff):
                h = str(hex(c))
                h = h[2:]
                while(len(h) < 8):
                    h = '0' + h
                v += '\\U' + h
            else:
                raise Exception(
                    'IniWriter: string has invalid characters', string)
        return "'" + v + "'"

    def comment_tab(self, tab=None):
        if(tab is None):
            self.__comment_tab = self.__COMMENT_TAB
            return
        if(not isinstance(tab, int) or (int < 0)):
            raise Exception(
                'IniWriter.comment_tab(): argument positive integer', tab)
        self.__comment_tab = tab

    def delimiters(self, comment=None, key=None, value=None):
        if(comment):
            if(comment == ';'):
                self.__comment_delim = self.__COMMENT_DELIM_SEMI
            elif(comment == '#'):
                self.__comment_delim = self.__COMMENT_DELIM_HASH
            else:
                raise Exception(
                    'IniWriter.comment_delimiters(): comment argument must be semicolon(;) or hash(#)', comment)
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
        self.__validate_name(name)
        self.__lines.append(
            [self.__SECTION, name, self.__normalize_comment(comment)])

    def key(self, name, varg, comment=None):
        self.__validate_name(name)
        if(isinstance(varg, list)):
            values = varg
        else:
            values = [varg]
        vlist = []
        for value in values:
            if(value == True):
                v = 'true'
            elif(value == False):
                v = 'false'
            elif(value is None):
                v = 'none'
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
        self.__lines.append(
            [self.__COMMENT, self.__normalize_comment(comment)])

    def write(self, fname):
        with open(fname, 'r') as fd:
            fd.write(self.to_string())

# key line      = [id, name, value, comment]
# section line  = [id, name, comment]
# comment line  = [id, comment]
    def to_string(self):
        out = ''
        for line in self.__lines:
            if(line[0] == self.__COMMENT):
                if(line[1] == ''):
                    out += '\n'
                else:
                    if(line[1] is None):
                        out += self.__LINE_END
                    else:
                        out += self.__comment_delim + line[1] + self.__LINE_END
            elif(line[0] == self.__KEY):
                out += line[1] + self.__key_delim
                count = 0
                for v in line[2]:
                    if(count > 0):
                        out += self.__value_delim
                    out += v
                    count += 1
                out += self.__LINE_END
            else:
                out += '[' + line[1] + ']' + self.__LINE_END
        return out
