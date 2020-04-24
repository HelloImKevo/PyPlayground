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

presidents: list = ['Washington', 'Adams', 'Jefferson', 'Clinton', 'Bush', 'Obama', 'Trump']
for num, name in enumerate(presidents, start=1):
    print("President {}: {}".format(num, name))

print('Working with Dictionaries...')
colors: dict = dict(aquamarine='#7FFFD4', burlywood='#DEB887',
                    chartreuse='#7FFF00', cornflower='#6495ED',
                    firebrick='#B22222', honeydew='#F0FFF0',
                    maroon='#B03060', sienna='#A0522D')

for key in colors:
    print(f"{key} => {colors[key]}")

for value in colors.values():
    print(value)

for key in colors.keys():
    print(key)

# Traverse dictionary as item tuples
for key, value in colors.items():
    print(f"{key} => {colors[key]}")

print('aquamarine' in colors)
print('emerald' not in colors)

print('Working with Sets...')
blue_eyes: set = {'Olivia', 'Harry', 'Lily', 'Jack', 'Amelia'}
blond_hair: set = {'Harry', 'Jack', 'Amelia', 'Mia', 'Joshua'}
# People that can smell hydrogen cyanide
smell_hcn: set = {'Harry', 'Amelia'}
# People that can taste phenylthiocarbamide
taste_ptc: set = {'Harry', 'Lily', 'Amelia', 'Lola'}
o_blood: set = {'Mia', 'Joshua', 'Lily', 'Olivia'}
b_blood: set = {'Amelia', 'Jack'}
a_blood: set = {'Harry'}
ab_blood: set = {'Joshua', 'Lola'}
print(blue_eyes.union(blond_hair))
print(blue_eyes.union(blond_hair) == blond_hair.union(blue_eyes))
# Find all people with blond hair and blue eyes (intersection collects only
# elements that are present in both sets). This is commutative.
print(blue_eyes.intersection(blond_hair))
print(blue_eyes.intersection(blond_hair) == blond_hair.intersection(blue_eyes))
# Find all the people with blond hair and don't have blue eyes
print(blond_hair.difference(blue_eyes))
# People that have exclusively blond hair OR blue eyes, but not both
print(blond_hair.symmetric_difference(blue_eyes))
# Check if all people that can smell HCL have blond hair
print(smell_hcn.issubset(blond_hair))
# Check if all elements of the second set are present in the first set
print(taste_ptc.issuperset(smell_hcn))
# Check if these have no members in common
print(a_blood.isdisjoint(o_blood))

# Protocols: Container, Sized, Iterable, Sequence,
# Mutable Sequence, Mutable Set, Mutable Mapping
