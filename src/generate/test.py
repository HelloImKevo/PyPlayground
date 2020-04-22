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

    user_data: UserData = UserData(first_names, last_names)

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
