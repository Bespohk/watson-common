# -*- coding: utf-8 -*-
from watson.common.decorators import cached_property, instance_set


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


class TestBoundDecorator(object):

    def test_bound_kwargs(self):
        class MyClass(object):

            @instance_set
            def __init__(self, value='Test'):
                pass
        c = MyClass()
        assert c.value == 'Test'

    def test_bound_args(self):
        class MyClass(object):

            @instance_set
            def __init__(self, test, value='Test'):
                pass
        c = MyClass('testing')
        assert c.value == 'Test'
        assert c.test == 'testing'

    def test_ignore_bound(self):
        class MyClass(object):

            @instance_set(ignore=('value',))
            def __init__(self, value='Test'):
                pass
        c = MyClass()
        assert not hasattr(c, 'value')

    def test_inherited_bound(self):
        class MyClass(object):
            def __init__(self, value='Test'):
                self.value = value
                print('setting value')

        class InheritedClass(MyClass):
            @instance_set
            def __init__(self, testing='Something'):
                super(InheritedClass, self).__init__()
        c = InheritedClass()
        assert c.testing == 'Something'
        assert c.value == 'Test'
