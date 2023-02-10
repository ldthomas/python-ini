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
from apg_py.lib import utilities as utils
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

    def __validate_comment(self, comment):
        if(comment and isinstance(comment, str)):
            for s in comment:
                c = ord(s)
                if(c >= 32 and c <= 126):
                    continue

                # invalid character in comment
                line_no = len(self.__lines)
                self.errors.append(
                    'line: ' +
                    str(line_no) +
                    'invalid comment character, char code(' + str(c) + ')')
                return False
            return True

        # invalid comment string
        line_no = len(self.__lines)
        self.errors.append(
            'line: ' +
            str(line_no) +
            'comment is missing, empty or not a string')
        return False

    def __validate_name(self, name):
        if(name and isinstance(name, str)):
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
                line_no = len(self.__lines)
                self.errors.append(
                    'line: ' +
                    str(line_no) +
                    'invalid name character, char code(' + str(c) + ')')
                return False
            return True

        # invalid name string
        line_no = len(self.__lines)
        self.errors.append(
            'line: ' +
            str(line_no) +
            'name is missing, empty or not a string')
        return False

    def comment_delim(self, delim):
        if(delim == ';'):
            self.__comment_delim = __COMMENT_DELIM_SEMI
        elif(delim == ';'):
            self.__comment_delim = __COMMENT_DELIM_HASH
        else:
            line_no = len(self.__lines)
            self.errors.append(
                'line: ' +
                str(line_no) +
                'comment delimiter must be semicolon(;) or hash(#)')

    def key_delim(self, delim):
        if(delim == '='):
            self.__key_delim = __KEY_DELIM_EQUALS
        elif(delim == ':'):
            self.__key_delim = __KEY_DELIM_COLON
        elif(delim == ' '):
            self.__key_delim = __KEY_DELIM_SPACE
        else:
            line_no = len(self.__lines)
            self.errors.append(
                'line: ' +
                str(line_no) +
                'key delimiter must be equals(=), colon(:) or space( )')

    def value_delim(self, delim):
        if(delim == ','):
            self.__value_delim = __VALUE_DELIM_COMMA
        elif(delim == ' '):
            self.__value_delim = __VALUE_DELIM_SPACE
        else:
            line_no = len(self.__lines)
            self.errors.append(
                'line: ' +
                str(line_no) +
                'value delimiter must be comma(,) or space( )')

    def section(self, name, comment=None):
        if(self.__validate_name(name)):
            com = ''
            if(self.__validate_comment(comment)):
                com = comment
            self.__lines.append([__SECTION, name, com])

    def key(self, name, value, comment=None):
        return

    def comment(self, comment):
        if(self.__validate_comment(comment)):
            self.__lines.append([__COMMENT, comment])

    def display_errors(self):
        return

    def to_string(self):
        return

    def write(self, fname):
        return
