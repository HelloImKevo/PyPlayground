#!/usr/bin/env python3

"""
Pluralsight Course
Core Python: Getting Started
by Austin Bingham

Retrieve and print words from a URL.

Usage:

    python3 core_words.py <URL>

    from core_words import *
    main("http://sixty-north.com/c/t.txt")
"""

import sys
from urllib.request import urlopen


def fetch_words(url: str) -> list:
    """
    Fetch a list of words from a URL.

    :param url: The URL of a UTF-8 text document.
    Example: http://sixty-north.com/c/t.txt
    :return: A list of strings containing the words from the document.
    """
    story = urlopen(url)
    story_words = []
    for line in story:
        line_words = line.decode('utf8').split()
        for word in line_words:
            story_words.append(word)

    story.close()
    return story_words


def print_items(items: list):
    """
    Print items, one per line.

    :param items: An iterable series of printable items.
    """
    for item in items:
        print(item)


def main(url: str):
    """
    Print each word from a text document from at a URL.

    :param url: The URL of a UTF-8 text document.
    """
    words = fetch_words(url)
    print_items(words)


'''
Useful Python references:

type(core_words) -> <class 'module'>

dir(core_words) -> list of all methods (LEGB: Local, Enclosing, Global, Built-in)

type(core_words.fetch_words) -> <class 'function'>

dir(core_words.fetch_words) -> list of all properties of the function

core_words.fetch_words.__doc__ -> docstring for the function
'''

if __name__ == '__main__':
    if sys.argv is not None and len(sys.argv) > 1:
        # Assume this file is being executed from CLI or Python interpreter
        # The 0th arg is the module filename.
        main(sys.argv[1])
    else:
        # Assume this file is being executed within an IDE
        main("http://sixty-north.com/c/t.txt")
