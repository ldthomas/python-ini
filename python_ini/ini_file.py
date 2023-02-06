''' @file python_ini/ini_file.py
@brief The IniFile class for parsing an INI file into section/key/values.
@dir docs @brief Supplemental documentation files.
@dir python_ini @brief The IniFile class.
@dir examples @brief Several examples of using the IniFile class.
'''
import sys
import os
import copy
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.trace import Trace
from apg_py.lib.ast import Ast
import python_ini.grammar as grammar
import python_ini.parser_callbacks as pcb
import python_ini.ast_callbacks as acb

# Note: The SABNF syntax for the ini file parser is in grammar.abnf.
# The grammar object, grammar.py was generated with (assuming PyPI installation of apg-py)
# python3 apg-py -i python_ini/grammar.abnf


class IniFile:

    def __init__(self, values='s', debug=False):
        '''Ini file parser constructor.
        @param values Determines whether the "getter" functions", get_values() and get_section_values(),
        return a single value or a list of one or more values.
            - 's' (default) Only a single value is returned for a given key.
                If more than one value is defined for the key, only the
                last value is returned.
            - 'm' Keys are captured as a list of one or more values.
                If the same key appears more than once within a given section,
                the value(s) are appended to the previous list.
        @param debug If True, a trace of the parse is printed to stdout.
        '''
        if(not (values == 'm' or values == 's')):
            msg = 'values must be "s" (single-valued) or "m" (multi-valued)'
            raise Exception(msg, values)
        self.errors = None
        self.__parser = Parser(grammar)
        if(debug):
            Trace(self.__parser, mode='xc')
        self.__parser.add_callbacks({'line-end': pcb.line_end})
        self.__parser.add_callbacks({'bad-section-line': pcb.bad_section_line})
        self.__parser.add_callbacks({'bad-value-line': pcb.bad_value_line})
        self.__parser.add_callbacks({'bad-blank-line': pcb.bad_blank_line})
        self.__parser.add_callbacks({'u_unicode8': pcb.unicode8})
        self.__parser.add_callbacks({'u_unicode4': pcb.unicode4})
        self.__parser.add_callbacks({'u_hexadecimal': pcb.hexadecimal})
        self.__parser.add_callbacks({'u_escaped-error': pcb.escaped_error})
        self.__ast = Ast(self.__parser)
        self.__ast.add_callback('section-name', acb.section_name)
        self.__ast.add_callback('key-name', acb.key_name)
        self.__ast.add_callback('value', acb.value)
        self.__ast.add_callback('d-quoted-value', acb.d_value)
        self.__ast.add_callback('s-quoted-value', acb.s_value)
        self.__ast.add_callback('string', acb.string_value)
        self.__ast.add_callback('true', acb.true_value)
        self.__ast.add_callback('false', acb.false_value)
        self.__ast.add_callback('null', acb.null_value)
        self.__ast.add_callback('int', acb.int_value)
        self.__ast.add_callback('float', acb.float_value)
        self.__data = {}
        self.__data['values'] = values
        self.__data['current_section'] = None
        self.__data['current_key'] = None
        self.__data['global'] = {}
        self.__data['sections'] = {}

    def parse(self, fname=None, fhandle=None, fstr=None):
        '''Parse the input INI file.
        Parses the ini file, input as a file name, file handle or string.
        At least one of fname, fhandle or fstr must be supplied.
        If more than one, the first non-None value of fname, fhandle or fstr in that
        order is accepted. If none are supplied an Exception is raised.
        @param fname The name of the ini file to parse.
        @param fhandle A handle to an open ini file.
        @param fstr The ini file as a string.
        '''
        self.errors = None
        if(fname):
            with open(fname, 'r') as fd:
                input = fd.read()
        elif(fhandle):
            input = fhandle.read()
        elif(fstr):
            input = fstr
        else:
            msg = 'no input supplied, must supply fname, fhandle or fstr'
            self.errors = msg
            raise Exception(msg)
        data = {}
        data['line_no'] = 1
        data['errors'] = []
        data['skip_escaped_error'] = False
        data['skip_bad_key'] = False
        result = self.__parser.parse(
            utils.string_to_tuple(input), user_data=data)
        if(not result.success):
            # ABNF syntax is designed so that this should never happen
            msg = 'internal error - parser failed'
            msg += '\nuse IniFile(debug=True) for a trace of the parser'
            raise Exception(msg)
        if(len(data['errors'])):
            # display errors
            msg = ''
            for error in data['errors']:
                msg += '{'
                count = 0
                for key, value in error.items():
                    if(count > 0):
                        msg += ', '
                    msg += str(key) + ': ' + str(value)
                    count += 1
                msg += '}\n'
            self.errors = msg
            # raise Exception('ini file syntax errors found')
        self.__data['current_section'] = None
        self.__data['current_key'] = None
        self.__data['global'] = {}
        self.__data['sections'] = {}
        self.__ast.translate(self.__data)

    def display_errors(self):
        '''Converts any errors found in the INI file syntax to
        a human-readable ASCII string.
        @returns Returns the errors display or None if none are found.
        '''
        display = None
        if(self.errors):
            display = copy.copy(self.errors)
        return display

    def get_keys(self):
        '''Get a list of the global key names.
        @returns Returns a list, possibly empty, of global key names.
        '''
        keys = []
        for key, value in self.__data['global'].items():
            keys.append(key)
        return keys

    def get_values(self, key, default=None):
        '''Get the list of values for a global key name.
        @param key The name of the key to get values for.
        @param default The value to return if the key name is not found.
        The default value ignores the single- or multi-valued mode
        and is returned exactly as given to the user.
        It is the user's responsibility to supply a default that
        makes sense to his application.
        @returns Returns
            - default if the key name is not found
            - True if the key name list is empty (a default "true" flag)
            - the full list of values if the values switch, "m"(multiple), is set in the constructor
            - the last name in the list if the values switch, "s"(single), is set in the constructor
        '''
        values = self.__data['global'].get(key)
        if(values is None):
            return default
        if(self.__data['values'] == 'm'):
            if(len(values) == 0):
                return [True]
            return values
        if(len(values) == 0):
            return True
        return values[len(values) - 1]

    def get_sections(self):
        '''Get a list of the section names.
        @returns Returns a list, possibly empty, of section names.
        '''
        sections = []
        for key, value in self.__data['sections'].items():
            sections.append(key)
        return sections

    def get_section_keys(self, section):
        '''Get a list of key names in the named section.
        @param section The section name to find the key names in .
        @returns Returns a list, possibly empty, of key names.
        '''
        keys = []
        if(self.__data['sections'].get(section)):
            for key, value in self.__data['sections'][section].items():
                keys.append(key)
        return keys

    def get_section_values(self, section, key, default=None):
        '''Get a list of values for the named key in the named section.
        @param section The section name to find the key in.
        @param key The key name to find the list of values for.
        @param default The value to return if the section or key name is not found.
        The default value ignores the single- or multi-valued mode
        and is returned exactly as given to the user.
        It is the user's responsibility to supply a default that
        makes sense to his application.
        @returns Returns
            - default if the section or key name is not found
            - True if the key name list is empty (a default "true" flag)
            - the full list of values if the multiple values switch, "m", is set in the constructor
            - the last name in the list if the single value switch, "s", is set in the constructor
        '''
        if(self.__data['sections'].get(section) is None):
            return default
        values = self.__data['sections'][section].get(key)
        if(values is None):
            return default
        if(self.__data['values'] == 'm'):
            if(len(values) == 0):
                return [True]
            return values
        # to get here self.__data['values'] == 's'
        if(len(values) == 0):
            return True
        return values[len(values) - 1]
