''' @file python_ini/parser_callbacks.py
@brief The parser call back functions for the IniFile class.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import identifiers as id


def line_end(cb):
    if(cb['state'] == id.MATCH):
        cb['user_data']['line_no'] += 1


def bad_section_line(cb):
    if(cb['state'] == id.MATCH):
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': 'bad section definition'})


def bad_value_line(cb):
    if(cb['state'] == id.MATCH):
        if(cb['user_data']['skip_bad_key']):
            cb['user_data']['skip_bad_key'] = False
        else:
            cb['user_data']['errors'].append({'line': cb['user_data']['line_no'] - 1,
                                              'message': 'bad key/value definition'})


def bad_blank_line(cb):
    if(cb['state'] == id.MATCH):
        msg = 'invalid blank line, only white space and comments allowed'
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': msg})


def hex_digit(d):
    if(d >= 48 and d <= 57):
        return d - 48
    if(d >= 65 and d <= 72):
        return d - 55
    if(d >= 97 and d <= 102):
        return d - 87
    return None


def unicode8(cb):
    cb['state'] = id.NOMATCH
    cb['phrase_length'] = 0
    d = cb['input'][cb['phrase_index']]
    if(d != 85):
        return
    c = 0
    for i in range(1, 9):
        d = cb['input'][cb['phrase_index'] + i]
        v = hex_digit(d)
        if(v is None):
            msg = 'Unicode-32 value(\\Uhhhhhhhh) has invalid hex digit - char code(' + \
                str(d) + ')'
            cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                              'message': msg})
            cb['user_data']['skip_escaped_error'] = True
            cb['user_data']['skip_bad_key'] = True
            return
        c = 16 * c + v
    if(c >= 0xd800 and c <= 0xdfff):
        msg = 'Unicode-32 value(\\Uhhhhhhhh) - surrogates not allowed - x' + \
            hex(c)
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': msg})
        cb['user_data']['skip_escaped_error'] = True
        cb['user_data']['skip_bad_key'] = True
    elif(c > 0x10ffff):
        msg = 'Unicode-32 value(\\Uhhhhhhhh) - value out of range - ' + \
            hex(c)
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': msg})
        cb['user_data']['skip_escaped_error'] = True
        cb['user_data']['skip_bad_key'] = True
    else:
        # successful match
        cb['state'] = id.MATCH
        cb['phrase_length'] = 9


def unicode4(cb):
    cb['state'] = id.NOMATCH
    cb['phrase_length'] = 0
    d = cb['input'][cb['phrase_index']]
    if(d != 117):
        return
    c = 0
    for i in range(1, 5):
        d = cb['input'][cb['phrase_index'] + i]
        v = hex_digit(d)
        if(v is None):
            msg = 'Unicode-16 value(\\uhhhh) has invalid hex digit - char code(' + \
                str(d) + ')'
            cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                              'message': msg})
            cb['user_data']['skip_escaped_error'] = True
            cb['user_data']['skip_bad_key'] = True
            return
        # validate the value
        c = 16 * c + v
    if(c >= 0xd800 and c <= 0xdfff):
        msg = 'Unicode-16 value(\\uhhhh) - surrogates not allowed - ' + \
            hex(c)
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': msg})
        cb['user_data']['skip_bad_key'] = True
        cb['user_data']['skip_escaped_error'] = True
    else:
        # successful match
        cb['state'] = id.MATCH
        cb['phrase_length'] = 5


def hexadecimal(cb):
    cb['state'] = id.NOMATCH
    cb['phrase_length'] = 0
    d = cb['input'][cb['phrase_index']]
    if(d != 120):
        return
    for i in range(1, 3):
        d = cb['input'][cb['phrase_index'] + i]
        v = hex_digit(d)
        if(v is None):
            msg = 'hexadecimal value(\\xhh) has invalid hex digit - char code(' + \
                str(d) + ')'
            cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                              'message': msg})
            cb['user_data']['skip_bad_key'] = True
            cb['user_data']['skip_escaped_error'] = True
            return
    # successful match
    cb['state'] = id.MATCH
    cb['phrase_length'] = 3


def escaped_error(cb):
    cb['state'] = id.NOMATCH
    cb['phrase_length'] = 0
    if(cb['user_data']['skip_escaped_error']):
        cb['user_data']['skip_escaped_error'] = False
    else:
        d = cb['input'][cb['phrase_index']]
        msg = 'unrecognized escaped character(\\c) - char code c(' + \
            str(d) + ')'
        cb['user_data']['errors'].append({'line': cb['user_data']['line_no'],
                                          'message': msg})
        cb['user_data']['skip_bad_key'] = True
