# -*- coding: utf-8 -*-
from pytest import raises
from watson.common import imports
from tests.watson.common.support import some_func


class TestImports(object):

    def test_qualified_name(self):
        self_name = imports.get_qualified_name(self)
        func_name = imports.get_qualified_name(some_func)
        assert 'tests.watson.common.test_imports.TestImports' == self_name
        assert 'tests.watson.common.support.some_func' == func_name

    def test_load_definition_from_string(self):
        data = imports.load_definition_from_string(
            'tests.watson.common.support.DATA')
        assert isinstance(data, dict)

    def test_load_invalid_definition(self):
        with raises(ImportError):
            imports.load_definition_from_string('invalid.module.Class')

    def test_from_cache(self):
        imports.load_definition_from_string('tests.watson.common.support.DATA')
        assert 'tests.watson.common.support.DATA' in imports.definition_lookup
