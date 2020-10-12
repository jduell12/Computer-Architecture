#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
print(cpu.registers)
print(cpu.ram)
print(cpu.pc)

# cpu.load()
# cpu.run()