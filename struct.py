from collections import namedtuple

def struct(name, slots, bases=()):
    """Mutable equivalent to namedtuple"""
    def init(self, *args, **kwargs):
        assert len(args) == len(slots)
        for slot, arg in zip(slots, args):
            setattr(self, slot, arg)
    def to_string(self):
        return name +'('+ ', '.join(
            slot +'='+ repr(getattr(self, slot)) for slot in slots
        ) +')'
    def to_namedtuple(self):
        if self.__class__._tuplecls is None:
            self.__class__._tuplecls = namedtuple(name, slots)
        return self.__class__._tuplecls(*(getattr(self, slot) for slot in slots))
    dct = {
        '__slots__': slots,
        '__init__':  init,
        '__repr__':  to_string,
        'tuple':     to_namedtuple,
        '_tuplecls': None
    }
    return type(name, bases, dct)