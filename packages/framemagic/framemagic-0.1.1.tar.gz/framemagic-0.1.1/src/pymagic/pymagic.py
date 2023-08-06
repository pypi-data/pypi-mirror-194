"""
PyMagic - a library that uses frames to analyze a call stack
"""
import dis
import random
import string
import sys

from multipledispatch import dispatch
from opcode import haslocal, hasconst, hasname, hasjrel, hascompare, hasfree, cmp_op
from types import CodeType, FunctionType

# noinspection SpellCheckingInspection
__all__ = ["getframe", "isfunctionincallchain", "nameof", "PropertyMeta"]


# noinspection SpellCheckingInspection
def _getframe(__depth=0):
    """Polyfill for built-in sys._getframe.

    :param __depth: deep of stack
    :return: Frame or None when __depth's frame in the top of stack.
    """

    if not isinstance(__depth, int):
        raise TypeError('an integer is required (got type %s)' % type(__depth))

    try:
        raise TypeError
    except TypeError:
        tb = sys.exc_info()[2]

    frame = tb.tb_frame.f_back
    del tb

    if __depth < 0:
        return frame

    try:
        while __depth:  # while i and frame: to disable the exception
            frame = frame.f_back
            __depth -= 1
    except AttributeError:
        raise ValueError('call stack is not deep enough')

    return frame


# noinspection PyUnresolvedReferences,SpellCheckingInspection,PyProtectedMember
getframe = sys._getframe if hasattr(sys, 'getframe') else _getframe


# noinspection SpellCheckingInspection
def isfunctionincallchain(obj, __depth=-1):
    """A function that determines whether the given function object
    or code object is in the call chain.

    :param obj: code object of function object
    :param __depth: search of deep
    :return: True or False
    """
    if not isinstance(obj, (CodeType, FunctionType)):
        raise TypeError('\'obj\' must be code or function')

    code = obj if not hasattr(obj, "__code__") else obj.__code__
    frame = getframe(1)
    while frame and __depth:
        if frame.f_code is code:
            return True

        __depth -= 1
        frame = frame.f_back

    return False


# noinspection SpellCheckingInspection,PyUnusedLocal
def nameof(obj):
    """A function that correctly determines the name of an object,
    without being tied to the object itself, for example:

    >>> var1 = [1,2]
    >>> var2 = var1
    >>> print(nameof(var1))
        var1
    >>> print(nameof(var2))
        var2
    :param obj: any object
    :return: name of object
    """
    frame = getframe(1)
    f_code, f_lineno = frame.f_code, frame.f_lineno

    for line in dis.findlinestarts(f_code):
        if f_lineno == line[1]:
            return _get_last_name(f_code.co_code[line[0]:frame.f_lasti], f_code)


# noinspection SpellCheckingInspection
def _get_argval(offset, op, arg, varnames=None, names=None, constants=None, cells=None):
    """Based on dis._get_instructions_bytes function.

    """

    # noinspection SpellCheckingInspection
    argval = None
    if arg is not None:
        argval = arg
        if op in haslocal:
            argval = varnames[arg]
        elif op in hasconst:
            argval = constants[arg]
        elif op in hasname:
            argval = names[arg]
        elif op in hasjrel:
            argval = offset + 2 + arg
        elif op in hascompare:
            argval = cmp_op[arg]
        elif op in hasfree:
            argval = cells[arg]
        elif op == dis.FORMAT_VALUE:
            argval, _ = dis.FORMAT_VALUE_CONVERTERS[arg & 0x3]
            argval = (argval, bool(arg & 0x4))

    return argval


def _get_last_name(code, f_code):
    arg, offset, op = None, None, None
    # noinspection PyProtectedMember
    for offset, op, arg in dis._unpack_opargs(code):
        pass

    if arg is None:
        return

    if op not in hasname:
        return _get_argval(offset, op, arg,
                           f_code.co_varnames,
                           f_code.co_names,
                           f_code.co_consts,
                           f_code.co_cellvars + f_code.co_freevars)

    return f_code.co_names[arg]


# noinspection PyMissingOrEmptyDocstring
class PropertyMeta(type):
    # noinspection SpellCheckingInspection
    """This meta class allows you to create simplified properties (like C#),
        for which you can use an ellipsis to indicate that the Python
        itself would create the desired accessor, for example:

        prop1 = property(..., ...)

        prop2 = property(fget=...,
                         fdel=...
        )

        @property
        def prop3(self):
            ...

        @property
        def prop4(self):
            pass

        @prop4.setter
        def prop4(self, value):
            pass

        @property
        def prop5(self):
            return

        In fact, a private field is created inside the class, through which the property works.

        """

    # noinspection SpellCheckingInspection,PySuperArguments
    def __init__(cls, name, bases, attrs):
        super(PropertyMeta, cls).__init__(name, bases, attrs)
        del_ns, set_ns = {}, {}

        @dispatch(str, namespace=del_ns)  # noqa: F811
        def deleter(fi):  # noqa: F811
            def _(self):
                if hasattr(self, fi):
                    delattr(self, fi)

            return _

        # deleter for overriding an existing deleter
        # noinspection SpellCheckingInspection
        @dispatch(type, FunctionType, str, namespace=del_ns)  # noqa: F811
        def deleter(cls_, fdel_, fi):
            ns = {}

            @dispatch([object], namespace=ns)
            def _(*args):
                return fdel_(*args)

            @dispatch(cls_, [object], namespace=ns)
            def _(self, *args):
                if hasattr(self, fi):
                    delattr(self, fi)

                return fdel_(self, *args)

            del ns

            return _

        def getter(fi):
            def _(self):
                return getattr(self, fi, None)

            return _

        @dispatch(str, namespace=set_ns)  # noqa: F811
        def setter(fi):  # noqa: F811
            def _(self, value):
                if getattr(self, fi, None) != value:
                    setattr(self, fi, value)

            return _

        # setter for properties with private setter
        @dispatch(str, (CodeType, type(None)), namespace=set_ns)  # noqa: F811
        def setter(fi, f_code):  # noqa: F811
            def _(self, value):
                frame = getframe(1)

                while frame:
                    # Cautious during debugging: if the stop point
                    # falls into the __init__ function, then its duplicate may
                    # be called and, as a result, the code objects will vary.
                    if f_code is frame.f_code:
                        return setattr(self, fi, value)

                    frame = frame.f_back

                raise AttributeError("'property' object has private setter")

            return _

        # setter for overriding an existing setter
        # noinspection SpellCheckingInspection
        @dispatch(type, FunctionType, str, namespace=set_ns)  # noqa: F811
        def setter(cls_, fset_, fi: str):  # noqa: F811
            ns = {}

            @dispatch([object], namespace=ns)
            def _(*args):
                for arg in args:
                    if isinstance(arg, cls_) and hasattr(arg, fi):
                        for arg_ in args:
                            if not isinstance(arg_, cls_) and getattr(arg, fi, None) != arg_:
                                setattr(arg, fi, arg_)
                                return fset_(*args)

                        break

                return fset_(*args)

            @dispatch(cls_, object, namespace=ns)
            def _(self, value):
                if getattr(self, fi, None) != value:
                    setattr(self, fi, value)
                    return fset_(self, value)

            del ns

            return _

        if hasattr(cls, '__dict__'):
            attrs.update(cls.__dict__)

        for key, obj in attrs.items():
            if not isinstance(obj, property):
                continue

            fget, fset, fdel = obj.fget, obj.fset, obj.fdel
            field = '_' + name + '__' + ''.join(random.choices(string.ascii_lowercase, k=10)) + '_' + key

            if _is_empty_accessor(fget):
                setattr(cls, field, None)
                fget = getter(field)

                if fdel is None:
                    fdel = Ellipsis

            if _is_empty_accessor(fset):
                setattr(cls, field, None)
                fset = setter(field)

                if fdel is None:
                    fdel = Ellipsis
            elif fset is None:  # for private setter (initialize in constructor of class)
                setattr(cls, field, None)
                fset = setter(field, cls.__init__.__code__ if hasattr(cls.__init__, '__code__') else None)

                if fdel is None:
                    fdel = Ellipsis
            elif hasattr(cls, field):
                fset = setter(cls, fset, field)

            if _is_empty_accessor(fdel):
                fdel = deleter(field)
            elif fdel is not None:
                fdel = deleter(cls, fdel, field)

            setattr(cls, key, property(fget, fset, fdel, obj.doc if hasattr(obj, 'doc') else None))
            del fdel, fget, fset, field

        del del_ns, set_ns
        del deleter, getter, setter


def _is_empty_accessor(accessor):
    """Accessor is empty if it is an ellipsis or an empty function.

    """
    if accessor is None:
        return False
    elif accessor is Ellipsis:
        return True

    code = getattr(accessor, '__code__', {'co_consts': (None,), 'co_names': ()})
    if len(code.co_consts) == 1 and not len(code.co_names):
        return True

    return False
