# -*- coding: utf-8 -*-
from watson.common import strings


class TestStrings(object):
    def test_hash(self):
        assert strings.hash('test_ing') == 'test-ing'
        assert strings.hash('test_ing', titlecase=True) == 'Test-Ing'

    def test_camelize(self):
        assert strings.camelcase('something_else', uppercase=False) == 'somethingElse'
        assert strings.camelcase('something_else') == 'SomethingElse'

    def test_underscore(self):
        assert strings.snakecase('SomethingElse') == 'something_else'

    def test_url_safe(self):
        assert strings.url_safe('Test Ing') == 'test-ing'
