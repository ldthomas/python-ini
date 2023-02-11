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

__SECTION = 0
__KEY = 1
__COMMENT = 2
__COMMENT_DELIM_SEMI = '; '
__COMMENT_DELIM_HASH = '# '
__COMMENT_TAB = 40
__KEY_DELIM_EQUALS = ' = '
__KEY_DELIM_COLON = ': '
__KEY_DELIM_SPACE = ' '
__VALUE_DELIM_COMMA = ', '
__VALUE_DELIM_SPACE = ' '
__NAME_CHARS = [33, 36, 37, 38, 40, 41, 42, 43, 45,
                46, 60, 62, 63, 64, 94, 95, 123, 124, 125, 126]


class IniWriter:

    def __init__(self):
        '''Ini file writer constructor.
        '''
        self.errors = []
        self.__lines = []
        self.__comment_delim = __COMMENT_DELIM_SEMI
        self.__key_delim = __KEY_DELIM_EQUALS
        self.__value_delim = __VALUE_DELIM_COMMA
        self.__comment_tab = __COMMENT_TAB

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
            if(c in __NAME_CHARS):
                continue

            # invalid character in name
            return False
        return True

    def comment_tab(self, tab=__COMMENT_TAB):
        if(not isinstance(tab, int) or (int < 0)):
            raise Exception(
                'IniWriter.comment_tab(): argument positive integer', tab)
        self.__comment_tab = tab

    def comment_delim(self, delim=';'):
        if(delim == ';'):
            self.__comment_delim = __COMMENT_DELIM_SEMI
        elif(delim == '#'):
            self.__comment_delim = __COMMENT_DELIM_HASH
        else:
            raise Exception(
                'IniWriter.comment_delim(): argument must be semicolon(;) or hash(#)', delim)

    def key_delim(self, delim='='):
        if(delim == '='):
            self.__key_delim = __KEY_DELIM_EQUALS
        elif(delim == ':'):
            self.__key_delim = __KEY_DELIM_COLON
        elif(delim.isspace()):
            self.__key_delim = __KEY_DELIM_SPACE
        else:
            raise Exception(
                'IniWriter.key_delim(): argument must be equals(=), comma(,) or space', delim)

    def value_delim(self, delim=','):
        if(delim == ','):
            self.__value_delim = __VALUE_DELIM_COMMA
        elif(delim.isspace()):
            self.__value_delim = __VALUE_DELIM_SPACE
        else:
            raise Exception(
                'IniWriter.value_delim(): argument must be comma(,) or space', delim)

    def section(self, name, comment=None):
        self.__validate_name(name)
        self.__lines.append(
            [__SECTION, name, self.__normalize_comment(comment)])

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
            elif(c == 34):
                v += '\\"'
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
        return v

    def key(self, name, value, comment=None):
        self.__validate_name(name)
        if(isinstance(value, int) or isinstance(value, float)):
            v = value
        elif(value == True or value == False or value is None):
            v = value
        elif(isinstance(value, str)):
            v = self.__normalize_string(value)
        else:
            raise Exception('IniWriter.key(): invalid value', value)
        self.__lines.append(
            [__KEY, name, v, self.__normalize_comment(comment)])

    def comment(self, comment):
        self.__lines.append([__COMMENT, self.__normalize_comment(comment)])

    def write(self, fname):
        with open(fname, 'r') as fd:
            fd.write(self.to_string())

    def to_string(self):
        return
