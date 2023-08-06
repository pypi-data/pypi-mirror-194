from inspect import Parameter, Signature, signature

from pycparser.c_ast import FuncDecl

try:
    from pycparserext.ext_c_generator import GnuCGenerator as CGenerator
    from pycparserext.ext_c_parser import FuncDeclExt
    from pycparserext.ext_c_parser import GnuCParser as CParser

    PCYPARSEREXT = True
except ImportError:
    from pycparser.c_generator import CGenerator
    from pycparser.c_parser import CParser

    PCYPARSEREXT = False


def is_FuncDecl(node):
    ret = False
    if PCYPARSEREXT:
        ret = ret or isinstance(node, FuncDeclExt)
    return ret or isinstance(node, FuncDecl)


def call(fun, **kwargs):
    sig: Signature = signature(fun)
    newargs = list()
    newkwargs = dict()
    for name, parameter in sig.parameters.items():
        if parameter.kind == Parameter.POSITIONAL_ONLY:
            raise ValueError("Changes in positional parameters cannot be fixed!")
        elif parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
            value = parameter.default if name not in kwargs else kwargs[name]
            newkwargs[name] = value
            continue
        elif parameter.kind in (
            Parameter.POSITIONAL_OR_KEYWORD,
            Parameter.KEYWORD_ONLY,
        ):
            newkwargs[name] = kwargs[name]
        elif parameter.kind == Parameter.VAR_POSITIONAL:
            continue
        elif parameter.kind == Parameter.VAR_KEYWORD:
            newkwargs.update(kwargs)
    return fun(**newkwargs)
