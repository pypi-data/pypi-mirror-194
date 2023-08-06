# keinsum

[![pypi](https://img.shields.io/pypi/v/keinsum.svg)](https://pypi.python.org/pypi/keinsum)
[![python](https://img.shields.io/pypi/pyversions/keinsum.svg)](https://pypi.org/project/keinsum/)
![Coverage Badge](img/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/pypi/l/keinsum)](https://pypi.org/project/keinsum/)

An extension of np.einsum where capital letters serve as multiple ellipses, see [Einsum Visualized](https://betterprogramming.pub/einsum-visualized-c050903145ef?sk=e05c7d70e150f91e29f3d0a37326e087) for details.

## Installation: 

    pip install keinsum

## Usage

`keinsum('Ik,kJ', a, b)` is the same as `np.einsum('ijk,klm', a, b)` where `a` and `b` are 3D arrays.

## Testing

Run `pytest` in the project root.
