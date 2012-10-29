import os
import inspect

def get_call_stack():
    return ["%s:%s.%s" % (e[1],e[3],e[2]) for e in inspect.stack()[1:]]

def log(message, *args):
   print 'LOG', message % args


def trace(full_function_name, function):
    def wrapper(*args, **kwargs):
        log("%s <- %s", full_function_name, get_call_stack()[1])
        return function(*args, **kwargs)
    return wrapper


class BaseMetaClass(type):
    config_file = None

    def __init__(cls, class_name, base_classes, attributes):
        for name in attributes:
            fullname = "%s:%s:%s"  % (cls.__module__, cls.__name__, name)
            setattr(cls, name, cls.wrap_class_method(fullname, name, attributes[name]))

    @classmethod
    def wrap_class_method(cls, fullname, name, value):
        if name.startswith("_") or not callable(value):
            return value
        return trace(fullname,value)

class BaseClass(object):
    __metaclass__ = BaseMetaClass



class Foo(BaseClass):
    def foo(self, n):
        return 1 / n

class Bar(BaseClass):
    def __init__(self):
        self.foo = Foo()
    def bar(self, n):
        self.foo.foo(n)


if __name__ == '__main__':
    foo = Foo()
    bar = Bar()
    foo.foo(42)
    bar.bar(23)


