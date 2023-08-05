#!/usr/bin/env python3
# Generated by "pythonizer -d5 -v3 -aM ../Class/Struct.pm" v1.024 run by SNOOPYJC on Fri Feb  3 17:13:12 2023
__author__ = """Joe Cool"""
__email__ = "snoopyjc@gmail.com"
__version__ = "1.024"
import builtins, itertools, perllib

_bn = lambda s: "" if s is None else s
_str = lambda s: "" if s is None else str(s)
perllib.init_package("Class.Struct", is_class=True)


def struct_(*_args):
    _args = list(_args)

    args = perllib.Hash()
    class_ = None
    i_l = 0
    ndx = None
    ndx_map = perllib.Hash()
    self = perllib.Array()
    base_type = (perllib.ref_scalar(_args[1])) if len(_args) >= 2 else ""
    package = None
    decls = perllib.Array()
    if base_type == "HASH":
        package = _args.pop(0) if _args else None
        decls = perllib.Array(itertools.chain.from_iterable(_args[0].items()))
    elif base_type == "ARRAY":
        package = _args.pop(0) if _args else None
        decls = _args[0].copy()
    else:
        base_type = "ARRAY"
        package = perllib.caller_s()
        decls = _args.copy()
    # print STDERR "base_type=$base_type, package=$package, decls=@decls\n";

    if base_type == "HASH":

        def _f35(*_args):
            _args = list(_args)
            nonlocal package

            class_ = (_args.pop(0) if _args else None) if len(_args) else package
            self = perllib.bless(perllib.Hash(), class_)
            args = perllib.Hash({_args[_i]: _args[_i + 1] for _i in range(0, len(_args), 2)})
            for _d in list(args.keys()):
                self[_str(_d)] = args.get(_str(_d))

            return self

        perllib.store_perl_global(
            f"{_bn(package)}::new", _f35, infer_suffix=True, method_type=True
        )
    else:
        ndx_map = perllib.Hash()
        for i_l in range(0, len(decls), 2):
            ndx_map[_str(decls[perllib.int_(i_l)])] = i_l >> 1

        perllib.store_perl_global(f"{_bn(package)}::_ndx_map" + "_h", ndx_map)

        def _f50(*_args):
            _args = list(_args)
            nonlocal package

            class_ = (_args.pop(0) if _args else None) if len(_args) else package
            self = perllib.bless(perllib.Array(), class_)
            args = perllib.Hash({_args[_i]: _args[_i + 1] for _i in range(0, len(_args), 2)})
            for _d in list(args.keys()):
                self[
                    perllib.int_(
                        perllib.fetch_perl_global(f"{_bn(package)}::_ndx_map" + "_h")[_d]
                    )
                ] = args.get(_str(_d))

            return self

        perllib.store_perl_global(
            f"{_bn(package)}::new", _f50, infer_suffix=True, method_type=True
        )

    for i_l in range(0, len(decls), 2):
        key = decls[perllib.int_(i_l)]
        val = decls[perllib.int_(i_l) + 1]
        # print STDERR "Handing $package $key => $val\n";
        if _str(val) == "$" or _str(val) == "*$":
            if base_type == "HASH":

                def _f66(key):
                    def _f66template(*_args):
                        _args = list(_args)
                        nonlocal key
                        self = _args.pop(0) if _args else None
                        if len(_args):
                            self[_str(key)] = _args[0]

                        return self.get(_str(key))

                    return _f66template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f66(key), infer_suffix=True
                )
            else:

                def _f74(key):
                    def _f74template(*_args):
                        _args = list(_args)
                        nonlocal key, package
                        self = _args.pop(0) if _args else None
                        ndx = perllib.fetch_perl_global(f"{_bn(package)}::_ndx_map" + "_h").get(
                            key
                        )
                        if len(_args):
                            self[perllib.int_(ndx)] = _args[0]

                        return self[perllib.int_(ndx)]

                    return _f74template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f74(key), infer_suffix=True
                )
        elif _str(val) == "@" or _str(val) == "*@":
            if base_type == "HASH":

                def _f85(key):
                    def _f85template(*_args):
                        _args = list(_args)
                        nonlocal key
                        self = _args.pop(0) if _args else None
                        if len(_args):
                            if perllib.refs(_args[0]) == "ARRAY":
                                self[_str(key)] = _args[0]
                            elif len(_args) == 1:
                                return self[_str(key)][perllib.int_(_args[0])]
                            else:
                                self[_str(key)][perllib.int_(_args[0])] = _args[1]
                                return _args[1]

                        return self.get(_str(key))

                    return _f85template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f85(key), infer_suffix=True
                )
            else:

                def _f100(key):
                    def _f100template(*_args):
                        _args = list(_args)
                        nonlocal key, package
                        self = _args.pop(0) if _args else None
                        ndx = perllib.fetch_perl_global(f"{_bn(package)}::_ndx_map" + "_h").get(
                            key
                        )
                        if len(_args):
                            if perllib.refs(_args[0]) == "ARRAY":
                                self[perllib.int_(ndx)] = _args[0]
                            elif len(_args) == 1:
                                return self[perllib.int_(ndx)][perllib.int_(_args[0])]
                            else:
                                self[perllib.int_(ndx)][perllib.int_(_args[0])] = _args[1]
                                return _args[1]

                        return self[perllib.int_(ndx)]

                    return _f100template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f100(key), infer_suffix=True
                )
        elif _str(val) == "%" or _str(val) == "*%":
            if base_type == "HASH":

                def _f118(key):
                    def _f118template(*_args):
                        _args = list(_args)
                        nonlocal key
                        self = _args.pop(0) if _args else None
                        if len(_args):
                            if perllib.refs(_args[0]) == "HASH":
                                self[_str(key)] = _args[0]
                            elif len(_args) == 1:
                                return self[_str(key)].get(_str(_args[0]))
                            else:
                                self[_str(key)][_str(_args[0])] = _args[1]
                                return _args[1]

                        return self.get(_str(key))

                    return _f118template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f118(key), infer_suffix=True
                )
            else:

                def _f133(key):
                    def _f133template(*_args):
                        _args = list(_args)
                        nonlocal key, package
                        self = _args.pop(0) if _args else None
                        ndx = perllib.fetch_perl_global(f"{_bn(package)}::_ndx_map" + "_h").get(
                            key
                        )
                        if len(_args):
                            if perllib.refs(_args[0]) == "HASH":
                                self[perllib.int_(ndx)] = _args[0]
                            elif len(_args) == 1:
                                return self[perllib.int_(ndx)].get(_str(_args[0]))
                            else:
                                self[perllib.int_(ndx)][_str(_args[0])] = _args[1]
                                return _args[1]

                        return self[perllib.int_(ndx)]

                    return _f133template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f133(key), infer_suffix=True
                )
        else:
            if base_type == "HASH":

                def _f151(key):
                    def _f151template(*_args):
                        _args = list(_args)
                        nonlocal key
                        self = _args.pop(0) if _args else None
                        if len(_args):
                            self[_str(key)] = _args[0]

                        return self.get(_str(key))

                    return _f151template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f151(key), infer_suffix=True
                )
            else:

                def _f159(key):
                    def _f159template(*_args):
                        _args = list(_args)
                        nonlocal key, package
                        self = _args.pop(0) if _args else None
                        ndx = perllib.fetch_perl_global(f"{_bn(package)}::_ndx_map" + "_h").get(
                            key
                        )
                        if len(_args):
                            self[perllib.int_(ndx)] = _args[0]

                        return self[perllib.int_(ndx)]

                    return _f159template

                perllib.store_perl_global(
                    f"{_bn(package)}::{_bn(key)}", _f159(key), infer_suffix=True
                )


Class.Struct.struct_ = struct_


def import_(*_args):
    _args = list(_args)
    class_ = _args[0]
    callpkg = perllib.caller_s()
    perllib.store_perl_global(f"{_bn(callpkg)}::struct", Class.Struct.struct_, infer_suffix=True)
    if len(_args) > 2:
        (_args.pop(0) if _args else None)
        __goto_sub__ = True
        return struct_(*_args)


Class.Struct.import_ = import_
builtins.__PACKAGE__ = "Class.Struct"

# SKIPPED: require Exporter;
Class.Struct.ISA_a = "Exporter".split()
Class.Struct.EXPORT_a = "struct".split()
