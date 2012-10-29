import inspect

def get_call_stack():
    return ["%s:%s.%s" % (e[1],e[3],e[2]) for e in inspect.stack()[1:]]

META_ATTRIBUTE = '__meta_attribute__'

class MetaClass(type):
    @classmethod
    def log(mcls, message, *args):
        print message % args

    @classmethod
    def log_write_access(mcls, cls_object, attribute):
        whoami = cls_object.__name__
        def set_value(self, value):
            mcls.log('set %s.%s from %s',whoami,attribute, get_call_stack()[1])
            setattr(self,  META_ATTRIBUTE + attribute, value)
        def get_value(self):
            return getattr(self, META_ATTRIBUTE + attribute)
        setattr(cls_object,attribute, property(get_value, set_value))

    def __init__(self, name, bases, attributes):
        for name in attributes.get('__monitor__',()):
            self.log_write_access(self, name)

