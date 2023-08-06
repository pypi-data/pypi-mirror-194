from itertools import chain

import numpy as np

__version__ = '0.3'

__all__ = ["keinsum"]


def parse(fmt, *arrs):
    if "->" in fmt:
        lhs, rhs = fmt.split("->")
    else:
        lhs, rhs = fmt, None
    ops = lhs.split(",")
    dims = {}
    for i, op in enumerate(ops):
        for ch in op:
            if ch.islower():
                dims[ch] = 1
            else:
                dim = arrs[i].ndim - (len(op) - 1)
                if ch in dims:
                    if dim != dims[ch]:
                        raise ValueError(f"Inconsistent number of dimensions for {ch}.")
                else:
                    dims[ch] = dim
    d = {}
    i = 0
    for k, v in sorted(dims.items(), key=lambda x: x[0].lower()):
        d[k] = [i] if v == 1 else list(range(i, i + v))
        i += v
    if rhs is not None:
        ops.append(rhs)
    try:
        res = [list(chain.from_iterable(d[ch] for ch in op)) for op in ops]
    except KeyError as exc:
        raise ValueError(f"The rhs index {exc.args[0]} is missing from lhs.")
    return res


def construct(fmt, *args):
    sublists = parse(fmt, *args)
    new_args = []
    for i, sublist in enumerate(sublists):
        if i < len(args):
            new_args.append(args[i])
        new_args.append(sublist)
    return new_args


def keinsum(fmt, *args, **kwargs):
    return np.einsum(*construct(fmt, *args), **kwargs)
