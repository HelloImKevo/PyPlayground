#!/usr/bin/env python3

"""
Generate a user account.

Usage:

    python3 user_account.py
"""

import io
import json
import logging
import random
import sys
import time


class UserData:
    first_names: list = None
    last_names: list = None

    def __init__(self, first_names: list, last_names: list):
        self.first_names = first_names
        self.last_names = last_names


class User:
    _seed: int = None

    _first_name: str = None
    _last_name: str = None
    _birth_year: int = None
    _domain: str = None
    _email_address: str = None
    _password: str = None

    def __init__(self, seed: int = None):
        self._seed = seed

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self._first_name == other._first_name and \
               self._last_name == other._last_name and \
               self._birth_year == other._birth_year

    def __str__(self):
        return str.format("{} {}, {}",
                          self._first_name,
                          self._last_name,
                          self._email_address)

    def generate(self, _data: UserData):
        if self._seed is None:
            raise ValueError('Seed is required')

        random.seed(self._seed)

        # First name
        self._first_name = self._random_element(_data.first_names)

        # Last name
        self._last_name = self._random_element(_data.last_names)

        # Birth year
        self._birth_year = random.randint(1950, 2000)

        # Domain
        self._domain = 'gmail'

        # Email
        name_bound: int = 4
        if len(self._first_name) <= 6:
            name_bound = 3
        elif len(self._first_name) <= 3:
            name_bound = 2
        print(str.format("Name={}, Len={}, Bound={}", self._first_name, len(self._first_name), name_bound))
        self._email_address = str.format("{}{}{}{}@{}.com",
                                         self._piece(self._first_name, name_bound),
                                         '_',
                                         self._piece(self._last_name, 7),
                                         str(self._birth_year)[2:],
                                         self._domain).lower()

    @staticmethod
    def _piece(element: str, min_bound: int) -> str:
        """Internal function."""
        return element[:min(min_bound, len(element))]

    @staticmethod
    def _random_element(elements: list):
        """Internal function."""
        return elements[random.randrange(len(elements))]


def text_file_to_list(file_name: str) -> list:
    try:
        text_file: io.TextIOWrapper = open(file_name, mode='r')
        if text_file is not None:
            results = list(text_file.read().splitlines())
            logging.debug(results)
            text_file.close()
            return results
    except FileNotFoundError:
        logging.debug(f"File '{file_name}' does not exist!")

    # Return an empty list
    return list()


def save_json_to_file(file_name: str, json_string: str):
    try:
        text_file = open(file_name, mode='w')
        if text_file is not None:
            text_file.write(json_string)
            text_file.close()
    except FileNotFoundError:
        logging.debug(f"File '{file_name}' does not exist!")


def load_users_json_file(file_name: str) -> list:
    try:
        text_file: io.TextIOWrapper = open(file_name, mode='r')
        if text_file is not None:
            # Results are loaded as a list of dictionaries
            json_dict_list = json.loads(text_file.read())
            users = list()
            for user_dict_element in json_dict_list:
                user: User = User()
                print(type(user_dict_element), user_dict_element)
                user.__dict__ = user_dict_element
                users.append(user)
            text_file.close()
            return users
    except FileNotFoundError:
        logging.debug(f"File '{file_name}' does not exist!")

    # Return an empty list
    return list()


def get_seed() -> int:
    return time.time_ns()


def to_json_string(objects: list) -> str:
    # json_string = json.dumps([ob.__dict__ for ob in list_name])
    return json.dumps([obj.__dict__ for obj in objects], indent=4)


# Begin main:
def main(seed: int, how_many: int):
    # logging.getLogger().setLevel(level=logging.DEBUG)

    if how_many < 1:
        raise ValueError(f"Illegal value: {how_many}")

    if how_many > 1000:
        raise ValueError(f"Value {how_many} is much too large!")

    first_names: list = text_file_to_list('first_names.txt')
    last_names: list = text_file_to_list('last_names.txt')

    if not first_names:
        raise ValueError("Missing required 'first_names.txt' file")

    if not last_names:
        raise ValueError("Missing required 'last_names.txt' file")

    user_data: UserData = UserData(first_names, last_names)
    users: list = list()

    for i in range(how_many):
        user: User = User(seed)
        user.generate(user_data)
        users.append(user)

        # Increment the input seed (so every user does not have same seed
        seed += 1

    users_json: str = to_json_string(users)
    save_json_to_file('account_results.txt', users_json)

    print("Saved users to 'account_results.txt'...\n" + users_json)

    users_loaded = load_users_json_file('account_results.txt')
    for user in users_loaded:
        print(type(user), user)


if __name__ == '__main__':
    if sys.argv is not None and len(sys.argv) > 2:
        # Assume this file is being executed from CLI or Python interpreter
        # The 0th arg is the module filename.
        main(seed=sys.argv[1], how_many=sys.argv[2])
    else:
        # Assume this file is being executed within an IDE
        main(get_seed(), 1)
