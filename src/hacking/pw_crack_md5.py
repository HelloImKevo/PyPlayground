#!/usr/bin/env python3

"""
|   ____               ____                     _      __  __  ____   ____
|  |  _ \ __      __  / ___| _ __   __ _   ___ | | __ |  \/  ||  _ \ | ___|
|  | |_) |\ \ /\ / / | |    | '__| / _` | / __|| |/ / | |\/| || | | ||___ \
|  |  __/  \ V  V /  | |___ | |   | (_| || (__ |   <  | |  | || |_| | ___) |
|  |_|      \_/\_/    \____||_|    \__,_| \___||_|\_\ |_|  |_||____/ |____/
|

Attempts to crack an MD5 hash using an existing password dictionary.

Source: Ethical Hacking using Python - by Edureka!

Usage:

    python3 pw_crack_md5.py <md5_hash_string> <dictionary_file>
"""

import hashlib
import logging
import sys


def main(pass_hash: str = None, word_list_file_name: str = None):
    # logging.getLogger().setLevel(level=logging.DEBUG)

    if not pass_hash:
        pass_hash = input("Enter MD5 hash: ")

    if not word_list_file_name:
        word_list_file_name = input("File name: ")

    flag = 0
    pass_file = None

    try:
        pass_file = open(word_list_file_name, "r")
    except FileNotFoundError:
        logging.error(f"File '{word_list_file_name}' does not exist!")
        exit(1)

    for word in pass_file:
        encoded_word = word.encode('utf-8')
        digest = hashlib.md5(encoded_word.strip()).hexdigest()

        logging.debug(word)
        logging.debug(digest)
        logging.debug(pass_hash)

        if digest == pass_hash:
            print("Password found")
            print("Password is " + word)
            flag = 1
            break

    if flag == 0:
        print("Password is not in the provided dictionary.")


if __name__ == '__main__':
    if sys.argv is not None and len(sys.argv) > 2:
        # Assume this file is being executed from CLI or Python interpreter
        # The 0th arg is the module filename.
        main(pass_hash=sys.argv[1], word_list_file_name=sys.argv[2])
    else:
        # Assume this file is being executed within an IDE
        main(pass_hash=None, word_list_file_name=None)
