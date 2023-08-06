from functools import partial
from json import loads
from os import environ
from unittest import TestCase
from unittest.mock import patch

from cast_from_env import cast_from, from_env


class UnitTests(TestCase):

    @patch.dict(environ, {'TEST_STR': 'a string', 'TEST_INT': '123', 'TEST_FLOAT': '12.34',
                          'TEST_TRUE': 'true', 'TEST_FALSE': 'no', 'TEST_JSON': '["this", 3, 2]'})
    def test_from_env(self):
        assertions(from_env)

    def test_cast_from(self):
        d = {'TEST_STR': 'a string', 'TEST_INT': '123', 'TEST_FLOAT': '12.34',
             'TEST_TRUE': 'true', 'TEST_FALSE': 'no', 'TEST_JSON': '["this", 3, 2]'}
        cf = partial(cast_from, getter=d.get)
        assertions(cf)


def assertions(fn):
    assert fn('NOT_SET') is None, 'Unset value returns None if no default'
    assert fn('NOT_SET', 'default') == 'default', 'Unset value returns default'
    assert fn('TEST_STR') == 'a string', 'Set value with no default returns string'
    assert type(fn('TEST_INT', 1)) is int, 'Value with int default is cast to int'
    assert type(fn('TEST_FLOAT', float)) is float, 'Value is cast to float'
    assert fn('TEST_TRUE', bool) is True, '"true" cast to bool is True'
    assert fn('TEST_FALSE', True) is False, '"no" cast to bool is False'
    assert fn('TEST_UNSET', True) is True, 'unset value cast to bool returns default'
    assert fn('TEST_JSON', loads) == ['this', 3, 2], 'JSON string is cast to array'
