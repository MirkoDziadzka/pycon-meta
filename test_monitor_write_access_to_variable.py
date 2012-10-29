
from monitor_write_to_variable import MetaClass

class Foo:
    __metaclass__ = MetaClass
    __monitor__ = ('counter',)

    def __init__(self):
        self.counter = 23
        self.name = 'foo'

    def do_something(self):
        self.counter += 1
        self.name = 'bar'


if __name__ == '__main__':
    foo = Foo()
    foo.do_something()
    print foo.counter
    foo.counter = 42
    print foo.counter

