#!/usr/bin/env python3

"""
|   _   _                       _                                      _
|  | | | | ___   ___  _ __     / \     ___   ___   ___   _   _  _ __  | |_
|  | | | |/ __| / _ \| '__|   / _ \   / __| / __| / _ \ | | | || '_ \ | __|
|  | |_| |\__ \|  __/| |     / ___ \ | (__ | (__ | (_) || |_| || | | || |_
|   \___/ |___/ \___||_|    /_/   \_\ \___| \___| \___/  \__,_||_| |_| \__|
|

Generate a user account.

Usage:

    python3 user_account.py <seed> <how_many>
"""

import io
import json
import logging
import random
import re
import sys
import time


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def get_random_element(elements: list):
        return elements[random.randrange(len(elements))]


class UserData:
    first_names: list = None
    last_names: list = None
    username_prefixes: list = None
    username_suffixes: list = None
    password_chunks: list = None
    topics: list = None

    def __init__(self, first_names: list, last_names: list,
                 username_prefixes: list, username_suffixes: list,
                 password_chunks: list, topics: list):
        self.first_names = first_names
        self.last_names = last_names
        self.username_prefixes = username_prefixes
        self.username_suffixes = username_suffixes
        self.password_chunks = password_chunks
        self.topics = topics

    def generate_username(self) -> str:
        rand_prefix = Utils.get_random_element(['The', ''])
        first_chunk = Utils.get_random_element(self.username_prefixes)
        second_chunk = Utils.get_random_element(self.username_suffixes)
        rand_sep = Utils.get_random_element(['x', '_', ''])
        rand_num = random.randint(1, 299)
        return str.format("{}{}{}{}{}", rand_prefix, first_chunk, rand_sep, second_chunk, rand_num)

    def generate_password(self) -> str:
        first_chunk = Utils.get_random_element(self.password_chunks)
        second_chunk = Utils.get_random_element(self.password_chunks)
        # Ensure the second chunk is unique from the first chunk
        while second_chunk is first_chunk:
            second_chunk = Utils.get_random_element(self.password_chunks)

        # Randomly capitalize characters
        first_chunk = ''.join(random.choice((str.upper, str.lower))(c) for c in first_chunk)
        second_chunk = ''.join(random.choice((str.upper, str.lower))(c) for c in second_chunk)

        # Random special character separator
        rand_sep = Utils.get_random_element(['!', '_', '(', ')', '*'])
        first_rand_num = random.randint(1, 9)
        second_rand_num = random.randint(1, 9)

        return str.format("{}{}{}{}{}",
                          first_chunk, first_rand_num, rand_sep, second_chunk, second_rand_num)

    def generate_phone(self):
        rand_zip = Utils.get_random_element([404, 909, 713, 951, 904, 305, 702])
        rand_first_part = random.randint(100, 999)
        rand_second_part = random.randint(1000, 9999)
        return str.format("({}) {}-{}", rand_zip, rand_first_part, rand_second_part)

    def get_random_topics(self, minimum: int, maximum: int) -> list:
        random_topics = list()
        how_many_topics = random.randint(minimum, maximum)
        for topic_index in range(how_many_topics):
            random_topic = Utils.get_random_element(self.topics)

            # Prevent duplicate topics in the list (Keep fetching random
            # topics until we have a unique one)
            while random_topic in random_topics:
                random_topic = Utils.get_random_element(self.topics)

            random_topics.append(random_topic)

        return random_topics


class User:
    _seed: int = None

    _first_name: str = None
    _last_name: str = None
    _birth_month: int = None
    _birth_day: int = None
    _birth_year: int = None
    _domain: str = None
    _email_address: str = None
    _username: str = None
    _password: str = None
    _state: str = None
    _phone_number: str = None
    _recovery_email: str = None
    _topics: list = None

    def __init__(self, seed: int = None):
        self._seed = seed

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self._first_name == other._first_name and \
               self._last_name == other._last_name and \
               self._birth_year == other._birth_year and \
               self._email_address == other._email_address

    def __str__(self):
        full_name = "{} {}".format(self._first_name, self._last_name)
        return str.format("{0: >20}, {1: >11}, {2: >26}, {3: >26}",
                          full_name,
                          self.get_birth_date(),
                          self._username,
                          self._email_address)

    def generate(self, user_data: UserData):
        if self._seed is None:
            raise ValueError('Seed is required')

        # We want pseudo-random generated users (but we want predictable
        # and reproducible values for future extension), so the random
        # utils get re-seeded for each step.
        random.seed(self._seed)

        # First name
        self._first_name = Utils.get_random_element(user_data.first_names)

        random.seed(self._seed + 1)

        # Last name
        self._last_name = Utils.get_random_element(user_data.last_names)

        random.seed(self._seed + 2)

        # Birth date
        self._birth_month = random.randint(1, 12)
        self._birth_day = random.randint(1, 28)
        self._birth_year = random.randint(1950, 2000)

        # Domain
        self._domain = 'mail'

        random.seed(self._seed + 3)

        # Email
        name_bound: int = 4
        if len(self._first_name) <= 6:
            name_bound = 3
        elif len(self._first_name) <= 3:
            name_bound = 2
        logging.debug(str.format("Name={}, Len={}, Bound={}", self._first_name, len(self._first_name), name_bound))
        # Site: https://www.mail.com/
        self._email_address = str.format("{}{}{}{}@{}.com",
                                         self._piece(self._first_name, name_bound),
                                         '.',
                                         self._piece(self._last_name, 7),
                                         str(self._birth_year)[1:],
                                         self._domain).lower()

        # Username
        random.seed(self._seed + 4)
        self._username = user_data.generate_username()

        # Password
        random.seed(self._seed + 5)
        self._password = user_data.generate_password()

        # State
        random.seed(self._seed + 6)
        self._state = Utils.get_random_element(['California', 'Alabama', 'Texas', 'Florida', 'Idaho', 'Oregon'])

        # TODO: Need to come up with a different phone number strategy - this is worthless
        # Phone Number
        random.seed(self._seed + 7)
        self._phone_number = user_data.generate_phone()

    def get_birth_date(self):
        return str.format("{}/{}/{}", self._birth_month, self._birth_day, self._birth_year)

    def get_email_address(self):
        return self._email_address

    def get_recovery_email(self):
        return self._recovery_email

    def set_recovery_email(self, recovery_email: str):
        self._recovery_email = recovery_email

    def set_topics(self, topics: list):
        self._topics = topics

    @staticmethod
    def _piece(element: str, min_bound: int) -> str:
        """Internal function."""
        return element[:min(min_bound, len(element))]


def text_file_to_list(file_name: str) -> list:
    try:
        text_file: io.TextIOWrapper = open(file_name, mode='r')
        if text_file is not None:
            results = list(text_file.read().splitlines())
            # Traverse a copy of the list to remove garbage elements
            # Remove empty elements and common comment conventions
            for result in results[:]:
                if not result \
                        or result.startswith('//') \
                        or result.startswith('#'):
                    results.remove(result)
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
                logging.debug(str.format("{} {}", type(user_dict_element), user_dict_element))
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


def apply_recovery_emails(users: list):
    for user in users:
        rand_recovery_email = Utils.get_random_element(users).get_email_address()

        # If there are multiple users, give each of them different recovery emails.
        if len(users) > 1:
            while rand_recovery_email == user.get_email_address():
                rand_recovery_email = Utils.get_random_element(users).get_email_address()

        user.set_recovery_email(rand_recovery_email)


def apply_topics(users: list, user_data: UserData):
    for user in users:
        user.set_topics(user_data.get_random_topics(minimum=4, maximum=7))


def too_similar(user_a: User, user_b: User) -> bool:
    # Check first and last name similarity
    if user_a._first_name == user_b._first_name:
        return True
    if user_a._last_name == user_b._last_name:
        return True

    username_a_chunks = re.findall('[A-Z][a-z]*', user_a._username)
    username_b_chunks = re.findall('[A-Z][a-z]*', user_b._username)
    for a_chunk in username_a_chunks:
        if a_chunk in username_b_chunks:
            # Username is too similar
            return True

    return False


def complex_enough(user: User) -> bool:
    return len(user._username) >= 13 \
           and len(user._email_address) >= 22


# Begin main:
def main(seed: int, how_many: int):
    # logging.getLogger().setLevel(level=logging.DEBUG)

    if how_many < 1:
        raise ValueError(f"Illegal value: {how_many}")

    if how_many > 1000:
        raise ValueError(f"Value {how_many} is much too large!")

    first_names: list = text_file_to_list('first_names.txt')
    last_names: list = text_file_to_list('last_names.txt')
    username_prefixes: list = text_file_to_list('username_prefixes.txt')
    username_suffixes: list = text_file_to_list('username_suffixes.txt')
    password_chunks: list = text_file_to_list('password_chunks.txt')
    topics: list = text_file_to_list('topics.txt')

    if not first_names:
        raise ValueError("Missing required 'first_names.txt' file")

    if not last_names:
        raise ValueError("Missing required 'last_names.txt' file")

    if not username_prefixes:
        raise ValueError("Missing required 'username_prefixes.txt' file")

    if not username_suffixes:
        raise ValueError("Missing required 'username_suffixes.txt' file")

    if not password_chunks:
        raise ValueError("Missing required 'password_chunks.txt' file")

    if not topics:
        raise ValueError("Missing required 'topics.txt' file")

    user_data: UserData = UserData(first_names, last_names,
                                   username_prefixes, username_suffixes,
                                   password_chunks, topics)
    users: list = list()

    iterations: int = 0
    while len(users) < how_many and iterations <= 200:
        user: User = User(seed)
        user.generate(user_data)

        # Check to make sure each user is distinct
        distinct: bool = True
        for existing in users:
            if too_similar(user, existing):
                distinct = False
                logging.debug(f"Discarding user: {user} - too similar to existing: {existing}")
                # Break from for loop
                break

        enough_complexity = complex_enough(user)
        if not enough_complexity:
            logging.debug(f"Discarding user: {user} - not complex enough")

        if distinct and enough_complexity:
            users.append(user)

        # Increment the input seed (each user must have a unique seed)
        seed += 1000
        iterations += 1

    if iterations > 200:
        raise ValueError(f"Unable to generate {how_many} unique users! "
                         f"Consider adding more data to the text files.")

    apply_recovery_emails(users)
    apply_topics(users, user_data)

    users_json: str = to_json_string(users)
    save_json_to_file('account_results.txt', users_json)

    print("\nSaved users to 'account_results.txt'...\n" + users_json)

    users_loaded = load_users_json_file('account_results.txt')
    print("\nLoaded users from text file:")
    for user in users_loaded:
        print(user)


if __name__ == '__main__':
    if sys.argv is not None and len(sys.argv) > 2:
        # Assume this file is being executed from CLI or Python interpreter
        # The 0th arg is the module filename.
        main(seed=int(sys.argv[1]), how_many=int(sys.argv[2]))
    else:
        # Assume this file is being executed within an IDE
        main(get_seed(), 1)
