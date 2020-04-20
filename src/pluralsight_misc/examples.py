#!/usr/bin/env python3

"""
Miscellaneous Pluralsight examples.
"""

import datetime
import math

print("Reticulating spline {} of {}.".format(4, 23))

# String formatting with a tuple
print("Galactic position x={pos[0]}, x={pos[1]}, z={pos[2]}"
      .format(pos=(65.2, 23.1, 82.2)))

# String formatting and import substitution and attribute reference
print("Math constants: pi={m.pi}, e={m.e}".format(m=math))

# String formatting with truncation / float precision
print("Math constants: pi={m.pi:.3f}, e={m.e:.3f}".format(m=math))

# PEP 498: Literal String Interpolation - Commonly called f-strings
print(f'The current time is {datetime.datetime.now().isoformat()}')
print(f'Math constants: pi={math.pi:.5f}, e={math.e:.5f}')

# Print all help docstrings for the string class (verbose)
# help(str)
