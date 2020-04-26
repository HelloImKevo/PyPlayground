import pytest
from user_account import UserData
from user_account import User
from user_account import text_file_to_list
from user_account import to_json_string


def sanity():
    print("Running test...")
    raise SystemExit(1)


# -------------------------------------------------------------------


def test_my_test():
    with pytest.raises(SystemExit):
        sanity()


# ----------------------------------------------------------------


def test_users():
    print("Running test...")

    first_names: list = text_file_to_list('first_names.txt')
    last_names: list = text_file_to_list('last_names.txt')
    username_prefixes: list = text_file_to_list('username_prefixes.txt')
    username_suffixes: list = text_file_to_list('username_suffixes.txt')
    password_chunks: list = text_file_to_list('password_chunks.txt')
    topics: list = text_file_to_list('topics.txt')

    user_data: UserData = UserData(first_names, last_names,
                                   username_prefixes, username_suffixes,
                                   password_chunks, topics)

    users: list = list()

    for seed in range(10):
        try:
            user: User = User(seed)
            user.generate(user_data)
            users.append(user)
        except Exception:
            raise SystemExit(-1)

    print(to_json_string(users))

    for index in range(len(users)):
        user: User = users[index]

        for comp_index in range(index + 1, len(users)):
            # print(f"Comparing {user} vs. {users[comp_index]}...")
            assert user is not users[comp_index]
            assert user != users[comp_index]


# ----------------------------------------------------------------


def test_user_uniqueness():
    print("Running test...")

    # Verify that all first names are unique
    first_names: list = text_file_to_list('first_names.txt')
    validate_list_uniqueness(first_names)

    # Verify that all last names are unique
    last_names: list = text_file_to_list('last_names.txt')
    validate_list_uniqueness(last_names)

    # Verify that all prefixes are unique
    validate_list_uniqueness(text_file_to_list('username_prefixes.txt'))

    # Verify that all suffixes are unique
    validate_list_uniqueness(text_file_to_list('username_suffixes.txt'))

    print("Elements in each list are unique.")


def validate_list_uniqueness(elements: list):
    for index in range(len(elements)):
        name = elements[index]

        for comp_index in range(index + 1, len(elements)):
            if elements[comp_index] == name:
                pytest.fail(f"Duplicate name found: {name}[{comp_index}]", pytrace=False)
