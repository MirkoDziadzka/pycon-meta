import os
import fnmatch

DEBUG_TARGETS = os.environ.get('DEBUG_TARGETS','').split(',')

def should_wrap(fullname):
    for pattern in DEBUG_TARGETS:
        if fnmatch.fnmatch(fullname, pattern):
            return True
    return False

def log(message, *args):
    print message % args

def trace_decorator(fullname, method):
    def wrapper(*args, **kwargs):
        log("%s CALL %s %s", fullname, args, kwargs)
        try:
            res =  method(*args, **kwargs)
            log("%s RETURN %s", fullname, res)
            return res
        except Exception,e:
            log("%s EXCEPTION %s", fullname, str(e))
            raise
    #...
    return wrapper

class BaseMetaClass(type):
    def __init__(self, class_name, base_classes, attributes):
        for name in attributes:
            if name.startswith('__'):
                continue
            fullname = "%s:%s:%s"  % (self.__module__, self.__name__, name)
            if should_wrap(fullname):
                setattr(self, name, trace_decorator(fullname, attributes[name]))

class BaseClass(object):
    __metaclass__ = BaseMetaClass



class Foo(BaseClass):
    def foo(self, n):
        return 1.0 / n

class Bar(BaseClass):
    def foo(self, n):
        return 1.0 / n

if __name__ == '__main__':
    foo = Foo()
    bar = Bar()
    foo.foo(3)
    foo.foo(4)
    bar.foo(3)
    foo.foo(0)

