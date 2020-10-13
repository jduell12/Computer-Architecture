#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
#prints ram as binary
# for ins in cpu.ram:
#     if ins == 0:
#         continue
#     print("{0:b}".format(ins))
cpu.run()