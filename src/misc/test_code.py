from math import *

# print("Hello World")

print("    /|")
print("   / |")
print("  /  |")
print(" /   |")
print("/____|")

character_name = "John"
character_age = "35"
print("There once was a man named " + character_name + ", ")
print("he was " + character_age + " years old. ")

character_name = "Mike"
print("He really liked the name " + character_name + ", ")
print("but didn't like being " + character_age + ".")

print("Giraffe\nAcademy")

phrase = "Giraffe Academy"
print(phrase + " is cool")

print(phrase.lower())
print(phrase.upper())
print(phrase.isupper())
print(len(phrase))
print(phrase[0])
print(phrase.index("G"))
print(phrase.replace("Giraffe", "Elephant"))

my_num = 5
print(str(my_num) + " my favorite number")

print((pow(8, 8)) / 16)

print(sqrt(49))

color = input("Enter a color: ")
plural_noun = input("Enter a plural noun: ")
celebrity = input("Enter a celebrity: ")

print("Roses are " + color)
print(plural_noun + " are blue")
print("I like " + celebrity)

# Tuples are immutable (you cannot alter the values)
coordinates = [(1, 2), (3, 4), (5, 6), (20, 30)]
# coordinates = (4, 5)
print(coordinates[0])
print(coordinates)

lucky_numbers = [4, 8, 15, 16, 23, 42]
friends = ["Kevin", "Karen", "Jim", "Oscar", "Toby"]
# print(friends[0])
# print(friends[-3])
print(friends[1:3])

# Append all lucky numbers to end of list
friends.extend(lucky_numbers)
print(friends)

# Add one element to end of list
friends.append("Creed")
print(friends)

friends.insert(1, "Kelly")

# print(_)

print(friends)

# print(friends.index("Mike"))
print(friends.__contains__("X"))

n = 5
for _ in range(n):
    print(".")


class C(object):
    def __mine__(self):
        pass


print(dir(C))

# num1 = input("Enter a number: ")
# num2 = input("Enter another number: ")
# result = float(num1) + float(num2)
# print(result)

# name = input("Enter your name: ")
# age = input("Enter your age: ")
# print("Hello " + name + "! You are " + age)
