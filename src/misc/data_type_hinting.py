def add_numbers(a: int, b: int) -> int:
    return a + b


def append_to_list(list_param: list, value: str):
    list_param.append(value)


def edit_dict(param: dict):
    try:
        del param["id"]
    except KeyError:
        print("Uh oh!")


print("Starting test...")
print(add_numbers(5, 2))
assert add_numbers(5, 2) == 7

names = ["Adam", "Bob", "Cathy"]

append_to_list(list_param=names, value="Daisy")
print(names)
assert names[3] == "Daisy"

x = 0
for index in range(5):
    x += 10
    print("The value of X is {0}".format(x))

student = {
    "name": "Mark",
    "student_id": 1500,
    "feedback": None
}

student["last_name"] = "Smith"

try:
    last_name = student["last_name"]
except KeyError:
    print("Error finding last_name")
except TypeError as error:
    print("I can't add these two together!")
    print(error)

print ("This code executes!")


def var_args(name: str=None, **kwargs):
    print(name)
    print(kwargs["description"], kwargs["feedback"])


var_args("Mark", description="Knows Python",
         feedback=None, subscriber=True)
