#!/usr/bin/env python3

import os
import sys

DIGIT_MAP: dict = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def convert(s):
    """Convert a string to an integer."""
    x = -1
    try:
        number = ''
        for token in s:
            number += DIGIT_MAP[token]
        x = int(number)
    except (KeyError, TypeError) as e:
        # Do nothing; ignore the exception
        # pass
        print(f"Conversion error: {e!r}", file=sys.stderr)
        # Re-raise the exception
        # raise
    return x


def sqrt(x) -> int:
    """
    Compute square roots using the method of
    Heron of Alexandria.

    :param x: The number for which the square root
    is to be computed.
    :return: The square root of x.

    :raises: ValueError if x is negative.
    """

    if x < 0:
        raise ValueError(
            "Cannot compute square root of "
            f"negative number {x}")

    guess = x
    i = 0
    while guess * guess != x and i < 20:
        guess = (guess + x / guess) / 2.0
        i += 1
    return guess


# Cleaning up after exceptions with finally:
def make_at(path, dir_name):
    original_path = os.getcwd()
    os.chdir(path)
    try:
        os.mkdir(dir_name)
    except OSError as e:
        print(e, file=sys.stderr)
        # Re-raise the exception
        raise
    finally:
        os.chdir(original_path)


def main():
    print("Testing numeric word string conversion...")
    print(convert("one three three seven".split()))
    print(convert("around two gajillion".split()))
    # noinspection PyTypeChecker
    print(convert(1568))

    print("Testing square root function...")
    try:
        print(sqrt(16))
        print(sqrt(9))
        print(sqrt(2))
        print(sqrt(-1))
        print("This is never printed.")
    except ValueError as e:
        print(e, file=sys.stderr)

    print("Program execution continues normally here.")

    # Python exception handling tenants:
    # LBYL: Look before you leap
    # EAFP: Easier to ask forgiveness than permission


if __name__ == '__main__':
    main()
