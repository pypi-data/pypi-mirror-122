#!/usr/bin/env python

# sfutils

"""Shotfile reading with pure python

https://www.aug.ipp.mpg.de/~git/pyaug/sfread.html

"""
__author__  = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.2.4'
__date__    = '07.10.2021'

import sys

from .sfread import *
from .sf2equ import *
from .libddc import ddcshotnr, previousshot
from .mapeq import *
from .ww import *
from .sfh import *

# Backward compatibility.

# On Windows, we encode and decode deep enough that something goes wrong and
# the encodings.utf_8 module is loaded and then unloaded, I don't know why.
# Adding a reference here prevents it from being unloaded.  Yuk.
import encodings.utf_8      # pylint: disable=wrong-import-position, wrong-import-order
