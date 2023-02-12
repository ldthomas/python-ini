import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
import unittest
from python_ini.ini_writer import IniWriter


class TestExceptions(unittest.TestCase):
    """Test all raised exceptions."""

    def test_comments(self):
        '''Normalization of comments execeptions.'''
        w = IniWriter()
        with self.assertRaises(Exception) as ctx:
            w.comment(10)
        # print()
        # print(ctx.exception)
        self.assertIn('ASCII', str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.comment('a\xffb')
        # print(ctx.exception)
        self.assertIn('char code(255)', str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.comment('a\tb')
        # print(ctx.exception)
        self.assertIn('char code(9)', str(ctx.exception))

    def test_strings(self):
        '''Key string values.'''
        w = IniWriter()
        with self.assertRaises(Exception) as ctx:
            w.key('name', 'a\ud800b')
        # print()
        # print(ctx.exception)
        self.assertIn('string has Unicode surrogate value', str(ctx.exception))

    def test_booleans(self):
        '''Set boolean values.'''
        w = IniWriter()
        with self.assertRaises(Exception) as ctx:
            w.booleans(true='TRUE')
            w.booleans(true='on')
            w.booleans(true='YeS')
            w.booleans(true='yep')
        # print()
        # print(ctx.exception)
        self.assertIn('yep', str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.booleans(false='FALSE')
            w.booleans(false='no')
            w.booleans(false='oFF')
            w.booleans(false='nope')
        # print(ctx.exception)
        self.assertIn('nope', str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.booleans(none='NONE')
            w.booleans(none='null')
            w.booleans(none='VoId')
            w.booleans(none='nill')
        # print(ctx.exception)
        self.assertIn('nill', str(ctx.exception))

    def test_comment_tab(self):
        '''Comment tab values.'''
        w = IniWriter()
        with self.assertRaises(Exception) as ctx:
            w.comment_tab(-10)
        # print()
        # print(ctx.exception)
        self.assertIn('argument must be positive integer', str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.comment_tab('10')
        # print(ctx.exception)
        self.assertIn('argument must be positive integer', str(ctx.exception))

    def test_delimiters(self):
        '''Setting delimiter values.'''
        w = IniWriter()
        with self.assertRaises(Exception) as ctx:
            w.delimiters(comment=10)
        # print()
        # print(ctx.exception)
        self.assertIn(
            'comment argument must be semicolon(;) or hash(#)',
            str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.delimiters(comment=':')
        # print(ctx.exception)
        self.assertIn(
            'comment argument must be semicolon(;) or hash(#)',
            str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.delimiters(key='#')
        # print(ctx.exception)
        self.assertIn(
            'key argument must be equals(=), comma(,) or space',
            str(ctx.exception))
        with self.assertRaises(Exception) as ctx:
            w.delimiters(value='#')
        # print(ctx.exception)
        self.assertIn(
            'value argument must be comma(,) or space',
            str(ctx.exception))

    def test_key_values(self):
        '''key values.'''
        w = IniWriter()
        with self.assertRaises(Exception) as ctx:
            w.key('name', {})
        # print()
        # print(ctx.exception)
        self.assertIn(
            'invalid value',
            str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
