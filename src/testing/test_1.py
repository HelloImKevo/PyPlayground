import pytest


def f():
    print("Running test...")
    raise SystemExit(1)


# -------------------------------------------------------------------

def test_my_test():
    with pytest.raises(SystemExit):
        f()


# -------------------------------------------------------------------

def func(x):
    return x + 1


# -------------------------------------------------------------------

def test_answer():
    assert func(3) == 5

