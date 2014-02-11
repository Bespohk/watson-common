# -*- coding: utf-8 -*-
from watson.common.decorators import cached_property


class TestCachedDecorator(object):

    def test_cached(self):

        class MyClass(object):

            @cached_property
            def expensive_prop(self):
                return 'This is an expensive call'

        c = MyClass()
        assert c.expensive_prop == 'This is an expensive call'
        assert hasattr(c, '_expensive_prop')
        del c._expensive_prop
        assert not hasattr(c, '_expensive_prop')
