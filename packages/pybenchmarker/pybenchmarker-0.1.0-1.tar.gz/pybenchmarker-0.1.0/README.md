# pybenchmarker
A simple utility for comparing the efficiency of functionally-equivalent
functions in Python.

## Installation
```
pip install pybenchmarker
```

## BenchmarkN class
**Problem**

<ul>

**Input**: two lists of equal length ``list_0``, ``list_1``.

**Output**: a *list* of booleans encoding which items of ``list_0`` are in
``list_1``.

</ul>

What's the fastest way to do this?
```Python
import numpy as np

from pybenchmarker import BenchmarkN, sizes
from random import randint


@sizes([2**k for k in range(18)])
def argfunc(n):
    return [randint(1, n) for i in range(n)], [randint(1, n) for i in range(n)]


def naive_lcomp(lists):
    return [x in lists[1] for x in lists[0]]


def set_other(lists):
    s = set(lists[1])
    return [x in s for x in lists[0]]


def numpy_isin(lists):
    return list(np.isin(lists[0], lists[1]))


if __name__ == '__main__':
    title = "list_3: list[bool], encoding which items in list_1 are in list_2"

    b = BenchmarkN(functions=[naive_lcomp, set_other, numpy_isin],
                   argfunc=argfunc)

    b.plot(xlabel="n", title=title, fname="my_figure", transparent=True,
           dpi=300)
```
This results in the following plot:

<!--Apparently, GitHub sanitizes inline styles, but the deprecated align
    attribute works.-->
<div align="center">
    <img src="https://github.com/OTheDev/pybenchmarker/raw/main/images/example.png"
         width="80%" height="80%">
</div>

## Inspiration
This project was inspired by [perfplot](https://github.com/nschloe/perfplot),
which was used to contribute to

- "[How do I efficiently find which elements of a list are in another list?](https://stackoverflow.com/questions/71990420/how-do-i-efficiently-find-which-elements-of-a-list-are-in-another-list)"
